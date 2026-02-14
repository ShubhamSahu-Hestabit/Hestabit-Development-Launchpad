import os
import json
import joblib
import logging
import numpy as np
import matplotlib.pyplot as plt
import warnings

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

# --------------------- CONFIG ---------------------
warnings.filterwarnings("ignore", category=UserWarning)  # ignore user warnings
import xgboost as xgb
xgb.set_config(verbosity=0)  # silence XGBoost info/warnings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "training.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Model training pipeline started")

# --------------------- LOAD DATA ---------------------
DATA_DIR = os.path.join(BASE_DIR, "features", "data", "processed")

X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))
y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

logger.info("Training and test datasets loaded")

# --------------------- DEFINE PIPELINES ---------------------
smote = SMOTE(random_state=42)

# Logistic Regression
lr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('smote', smote),
    ('model', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42))
])

# Random Forest
rf_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('smote', smote),
    ('model', RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=4,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ))
])

# XGBoost
xgb_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('smote', smote),
    ('model', XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1
    ))
])

# Neural Network
nn_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('smote', smote),
    ('model', MLPClassifier(
        hidden_layer_sizes=(128, 64),
        max_iter=1000,
        early_stopping=True,
        validation_fraction=0.2,
        random_state=42
    ))
])

# Stacking Ensemble
stack_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('smote', smote),
    ('model', StackingClassifier(
        estimators=[
            ('rf', rf_pipeline.named_steps['model']),
            ('xgb', xgb_pipeline.named_steps['model']),
            ('nn', nn_pipeline.named_steps['model'])
        ],
        final_estimator=LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
        cv=5,
        passthrough=True,
        n_jobs=-1
    ))
])

models = {
    "Logistic Regression": lr_pipeline,
    "Random Forest": rf_pipeline,
    "XGBoost": xgb_pipeline,
    "Neural Network": nn_pipeline,
    "Stacking Ensemble": stack_pipeline
}

# --------------------- TRAIN & EVALUATE ---------------------
scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
results = {}
best_model = None
best_score = 0.0
best_model_name = None

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    logger.info(f"Training model: {name}")
    
    # Cross-validation
    cv_results = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)
    
    # Fit on full training data
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1] if hasattr(model, "predict_proba") else y_pred
    
    metrics = {
        "cv_accuracy": float(np.mean(cv_results["test_accuracy"])),
        "cv_precision": float(np.mean(cv_results["test_precision"])),
        "cv_recall": float(np.mean(cv_results["test_recall"])),
        "cv_f1": float(np.mean(cv_results["test_f1"])),
        "cv_roc_auc": float(np.mean(cv_results["test_roc_auc"])),
        "test_accuracy": float(accuracy_score(y_test, y_pred)),
        "test_precision": float(precision_score(y_test, y_pred)),
        "test_recall": float(recall_score(y_test, y_pred)),
        "test_f1": float(f1_score(y_test, y_pred)),
        "test_roc_auc": float(roc_auc_score(y_test, y_proba))
    }
    
    results[name] = metrics
    logger.info(f"{name} - CV ROC-AUC: {metrics['cv_roc_auc']:.4f}")
    logger.info(f"{name} - Test ROC-AUC: {metrics['test_roc_auc']:.4f}")
    
    if metrics["cv_roc_auc"] > best_score:
        best_score = metrics["cv_roc_auc"]
        best_model = model
        best_model_name = name

# --------------------- SAVE BEST MODEL ---------------------
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))
logger.info(f"Best model saved: {best_model_name}")

# --------------------- SAVE METRICS ---------------------
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)
with open(os.path.join(EVAL_DIR, "metrics.json"), "w") as f:
    json.dump(results, f, indent=4)
logger.info("Metrics saved")

# --------------------- CONFUSION MATRIX ---------------------
y_pred_best = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_best)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title(f"Confusion Matrix - {best_model_name}")
plt.savefig(os.path.join(EVAL_DIR, "confusion_matrix.png"))
plt.close()
logger.info("Confusion matrix saved")

# --------------------- ROC CURVE ---------------------
y_proba_best = best_model.predict_proba(X_test)[:,1] if hasattr(best_model, "predict_proba") else y_pred_best
fpr, tpr, _ = roc_curve(y_test, y_proba_best)
roc_auc_val = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc_val:.2f})')
plt.plot([0,1], [0,1], color='red', linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title(f"ROC Curve - {best_model_name}")
plt.legend(loc="lower right")
plt.savefig(os.path.join(EVAL_DIR, "roc_curve.png"))
plt.close()
logger.info("ROC curve saved")
