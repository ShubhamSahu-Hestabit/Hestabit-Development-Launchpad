import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from lightgbm import LGBMClassifier
import optuna
from optuna.samplers import TPESampler

# ============================
# PATHS
# ============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
TUNING_DIR = os.path.join(BASE_DIR, "src", "tuning")  # Save metrics.json here
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)
os.makedirs(TUNING_DIR, exist_ok=True)

# ============================
# LOAD DATA
# ============================
print("="*80)
print("LOADING DATA")
print("="*80)
X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))
y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

print(f"Train: {X_train.shape}, Test: {X_test.shape}")
print(f"Train dist: {np.bincount(y_train.astype(int))}")
print(f"Test dist: {np.bincount(y_test.astype(int))}")

# ============================
# APPLY SMOTE
# ============================
print("\nApplying SMOTE...")
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)
print(f"After SMOTE: {X_train.shape}, dist: {np.bincount(y_train.astype(int))}")

y_train = y_train.astype(np.int32)
y_test = y_test.astype(np.int32)

# ============================
# CROSS-VALIDATION SETUP
# ============================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ============================
# OPTUNA TUNING FUNCTION
# ============================
def tune_lgbm(X_train, y_train, cv, n_trials=10):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 200, 600),
            'max_depth': trial.suggest_int('max_depth', 4, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
            'num_leaves': trial.suggest_int('num_leaves', 20, 80),
            'min_child_samples': trial.suggest_int('min_child_samples', 10, 50),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 2.0),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 2.0),
            'class_weight': 'balanced',
            'random_state': 42,
            'n_jobs': -1,
            'verbosity': -1
        }
        model = LGBMClassifier(**params)
        score = cross_val_score(model, X_train, y_train, cv=cv, scoring='roc_auc', n_jobs=-1)
        return score.mean()

    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=42))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

    print(f"\n[Optuna] Best CV ROC-AUC: {study.best_value:.4f}")
    print("[Optuna] Best Hyperparameters:")
    for k, v in study.best_params.items():
        print(f"  {k}: {v}")

    return study.best_params, study.best_value

# ============================
# TUNE LIGHTGBM
# ============================
print("\nTuning LightGBM with Optuna...")
best_params, best_cv_roc = tune_lgbm(X_train, y_train, cv, n_trials=10)

# ============================
# TRAIN BEST LIGHTGBM
# ============================
print("\nTraining LightGBM with best parameters...")
best_model = LGBMClassifier(**best_params)
best_model.fit(X_train, y_train)

y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

# ============================
# EVALUATE METRICS
# ============================
test_acc = accuracy_score(y_test, y_pred)
test_prec = precision_score(y_test, y_pred, zero_division=0)
test_rec = recall_score(y_test, y_pred, zero_division=0)
test_f1 = f1_score(y_test, y_pred, zero_division=0)
test_roc = roc_auc_score(y_test, y_proba)

# Compute CV metrics for the best model
from sklearn.model_selection import cross_validate
scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
cv_results = cross_validate(best_model, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1, return_train_score=True)
cv_acc = np.mean(cv_results["test_accuracy"])
cv_prec = np.mean(cv_results["test_precision"])
cv_rec = np.mean(cv_results["test_recall"])
cv_f1 = np.mean(cv_results["test_f1"])
cv_roc = np.mean(cv_results["test_roc_auc"])
train_roc = np.mean(cv_results["train_roc_auc"])

overfit_gap = train_roc - cv_roc
cv_test_gap = abs(cv_roc - test_roc)

# ============================
# PRINT RESULTS
# ============================
print("\n" + "="*80)
print("LIGHTGBM EVALUATION")
print("="*80)
print(f"CV ROC-AUC   : {cv_roc:.4f}")
print(f"Test ROC-AUC : {test_roc:.4f}")
print(f"Overfit Gap  : {overfit_gap:.4f}")
print(f"CV-Test Gap  : {cv_test_gap:.4f}")
print(f"Test Accuracy : {test_acc:.4f}")
print(f"Test Precision: {test_prec:.4f}")
print(f"Test Recall   : {test_rec:.4f}")
print(f"Test F1 Score : {test_f1:.4f}")

# ============================
# SAVE MODEL AND METRICS IN REQUIRED FORMAT
# ============================
results = {
    "LightGBM": {
        "cv_accuracy": cv_acc,
        "cv_precision": cv_prec,
        "cv_recall": cv_rec,
        "cv_f1": cv_f1,
        "cv_roc_auc": cv_roc,
        "test_accuracy": test_acc,
        "test_precision": test_prec,
        "test_recall": test_rec,
        "test_f1": test_f1,
        "test_roc_auc": test_roc,
        "overfit_gap": overfit_gap,
        "cv_test_gap": cv_test_gap
    }
}

# Save model
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_lgbm_model.pkl"))

RESULTS_FILE = os.path.join(BASE_DIR, "tuning", "results.json")  # final path
os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)  # ensure folder exists

with open(RESULTS_FILE, "w") as f:
    json.dump(results, f, indent=4)


print("\nSaved LightGBM model and metrics in tuning folder!")
print(f"Model: {MODEL_DIR}/best_lgbm_model.pkl")
print(f"Metrics: {RESULTS_FILE}")
