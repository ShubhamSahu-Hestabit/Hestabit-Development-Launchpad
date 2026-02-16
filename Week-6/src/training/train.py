import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import *
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)

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

# SMOTE
print("\nApplying SMOTE...")
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)
print(f"After SMOTE: {X_train.shape}, dist: {np.bincount(y_train.astype(int))}")

# Ensure y is integer (CRITICAL for XGBoost!)
y_train = y_train.astype(np.int32)
y_test = y_test.astype(np.int32)

# Models with REDUCED complexity to prevent overfitting
models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000, 
        C=0.5, 
        class_weight='balanced', 
        random_state=42
    ),
    
    "Random Forest": RandomForestClassifier(
        n_estimators=200,        # Reduced from 300
        max_depth=8,             # Reduced from 10
        min_samples_split=20,    # Increased
        min_samples_leaf=10,     # Increased
        max_features='sqrt',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ),
    
    "Neural Network": MLPClassifier(
        hidden_layer_sizes=(64, 32, 16),  # 3 hidden layers
        activation='relu',
        solver='adam',
        alpha=0.01,              # L2 regularization
        batch_size=128,
        learning_rate='adaptive',
        learning_rate_init=0.001,
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=20,
        random_state=42,
        verbose=False
    ),
    

    "LightGBM": LGBMClassifier(
        n_estimators=200,        # Reduced from 300
        max_depth=5,             # Limited depth
        learning_rate=0.05,
        num_leaves=20,           # Reduced from 31
        min_child_samples=30,    # Increased regularization
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1,
        verbosity=-1
    )
}

scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = {}
best_model, best_score, best_name = None, 0, None

print("\n"+"="*80)
print("TRAINING MODELS")
print("="*80)

for name, model in models.items():
    print(f"\n{name}...")
    
    try:
        cv_results = cross_validate(
            model, X_train, y_train, 
            cv=cv, 
            scoring=scoring, 
            n_jobs=-1, 
            return_train_score=True,
            error_score='raise'
        )
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        cv_acc = np.mean(cv_results["test_accuracy"])
        cv_prec = np.mean(cv_results["test_precision"])
        cv_rec = np.mean(cv_results["test_recall"])
        cv_f1 = np.mean(cv_results["test_f1"])
        cv_roc = np.mean(cv_results["test_roc_auc"])
        train_roc = np.mean(cv_results["train_roc_auc"])
        
        test_acc = accuracy_score(y_test, y_pred)
        test_prec = precision_score(y_test, y_pred, zero_division=0)
        test_rec = recall_score(y_test, y_pred, zero_division=0)
        test_f1 = f1_score(y_test, y_pred, zero_division=0)
        test_roc = roc_auc_score(y_test, y_proba)
        
        overfit_gap = train_roc - cv_roc
        cv_test_gap = abs(cv_roc - test_roc)
        
        print(f"  CV Metrics:")
        print(f"    Accuracy:  {cv_acc:.4f}")
        print(f"    Precision: {cv_prec:.4f}")
        print(f"    Recall:    {cv_rec:.4f}")
        print(f"    F1:        {cv_f1:.4f}")
        print(f"    ROC-AUC:   {cv_roc:.4f}")
        
        print(f"  Test Metrics:")
        print(f"    Accuracy:  {test_acc:.4f}")
        print(f"    Precision: {test_prec:.4f}")
        print(f"    Recall:    {test_rec:.4f}")
        print(f"    F1:        {test_f1:.4f}")
        print(f"    ROC-AUC:   {test_roc:.4f}")
        
        print(f"  Health:")
        print(f"    Overfit Gap: {overfit_gap:.4f} {'[HIGH]' if overfit_gap > 0.1 else '[OK]'}")
        print(f"    CV-Test Gap: {cv_test_gap:.4f} {'[HIGH]' if cv_test_gap > 0.05 else '[OK]'}")
        
        results[name] = {
            "cv_accuracy": float(cv_acc),
            "cv_precision": float(cv_prec),
            "cv_recall": float(cv_rec),
            "cv_f1": float(cv_f1),
            "cv_roc_auc": float(cv_roc),
            "test_accuracy": float(test_acc),
            "test_precision": float(test_prec),
            "test_recall": float(test_rec),
            "test_f1": float(test_f1),
            "test_roc_auc": float(test_roc),
            "overfit_gap": float(overfit_gap),
            "cv_test_gap": float(cv_test_gap)
        }
        
        if cv_roc > best_score:
            best_score, best_model, best_name = cv_roc, model, name
            print(f"  >> New best model!")
            
    except Exception as e:
        print(f"  [ERROR] {e}")
        import traceback
        traceback.print_exc()

# Table
print("\n"+"="*80)
print("COMPARISON TABLE")
print("="*80)
print(f"{'Model':<20} {'CV ROC':<10} {'Test ROC':<10} {'Test F1':<10} {'Test Prec':<10} {'Test Rec':<10} {'Gap':<10}")
print("-"*80)
for name, m in results.items():
    print(f"{name:<20} {m['cv_roc_auc']:<10.4f} {m['test_roc_auc']:<10.4f} {m['test_f1']:<10.4f} {m['test_precision']:<10.4f} {m['test_recall']:<10.4f} {m['cv_test_gap']:<10.4f}")

# Best model analysis
print("\n"+"="*80)
print(f"BEST MODEL: {best_name}")
print("="*80)

y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Failed", "Successful"]))

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
print(f"\nConfusion Matrix:")
print(f"  True Negatives:  {tn}")
print(f"  False Positives: {fp}")
print(f"  False Negatives: {fn}")
print(f"  True Positives:  {tp}")
print(f"\n  Specificity: {tn/(tn+fp):.4f}")
print(f"  Sensitivity: {tp/(tp+fn):.4f}")

# Save
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))
with open(os.path.join(EVAL_DIR, "metrics.json"), "w") as f:
    json.dump(results, f, indent=4)

# Plots
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Failed", "Successful"])
disp.plot(cmap='Blues')
plt.title(f"Confusion Matrix - {best_name}")
plt.tight_layout()
plt.savefig(os.path.join(EVAL_DIR, "confusion_matrix.png"), dpi=150)
plt.close()

fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure()
plt.plot(fpr, tpr, lw=2, label=f'AUC = {auc(fpr, tpr):.3f}', color='darkorange')
plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title(f"ROC Curve - {best_name}")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(EVAL_DIR, "roc_curve.png"), dpi=150)
plt.close()

print("\n"+"="*80)
print("FINAL SUMMARY - ALL METRICS")
print("="*80)
print(f"\nBest Model: {best_name}\n")

# Metrics Table
print(f"{'Metric':<20} {'CV Score':<12} {'Test Score':<12} {'Difference':<12}")
print("-"*80)

metrics_to_show = [
    ('Accuracy', 'accuracy'),
    ('Precision', 'precision'),
    ('Recall', 'recall'),
    ('F1 Score', 'f1'),
    ('ROC-AUC', 'roc_auc')
]

for metric_name, metric_key in metrics_to_show:
    cv_val = results[best_name][f'cv_{metric_key}']
    test_val = results[best_name][f'test_{metric_key}']
    diff = abs(cv_val - test_val)
    print(f"{metric_name:<20} {cv_val:<12.4f} {test_val:<12.4f} {diff:<12.4f}")

print("\n" + "-"*80)
print(f"{'Overfit Gap:':<20} {results[best_name]['overfit_gap']:.4f}")
print(f"{'CV-Test Gap:':<20} {results[best_name]['cv_test_gap']:.4f}")

if results[best_name]['cv_test_gap'] < 0.03:
    print("\n[EXCELLENT] Gap < 3% - No leakage!")
elif results[best_name]['cv_test_gap'] < 0.05:
    print("\n[GOOD] Gap < 5% - Minimal leakage")
else:
    print(f"\n[WARNING] Moderate gap ({results[best_name]['cv_test_gap']:.1%}) - Consider more regularization")

if results[best_name]['test_roc_auc'] >= 0.75:
    print("[TARGET ACHIEVED] Test ROC-AUC >= 75%!")
elif results[best_name]['test_roc_auc'] >= 0.70:
    print("[GOOD] Test ROC-AUC >= 70%")
else:
    print("[WARNING] Below 70% - Consider more features")

print("="*80)
print("\nTraining completed successfully!\n")