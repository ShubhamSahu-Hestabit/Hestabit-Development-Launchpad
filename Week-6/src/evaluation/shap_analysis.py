# /evaluation/shap_analysis.py

import os
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

# ============================
# PATHS
# ============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")  # Processed data folder
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_lgbm_model.pkl")  # From tuning
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)

# ============================
# LOAD DATA
# ============================
X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

# Load feature names if saved, else fallback
FEATURE_NAMES_PATH = os.path.join(DATA_DIR, "feature_names.npy")
if os.path.exists(FEATURE_NAMES_PATH):
    feature_names = np.load(FEATURE_NAMES_PATH, allow_pickle=True)
else:
    feature_names = [f"Feature {i+1}" for i in range(X_test.shape[1])]

# ============================
# LOAD MODEL
# ============================
model = joblib.load(MODEL_PATH)

# ============================
# SHAP EXPLAINER
# ============================
explainer = shap.Explainer(model, X_test)
shap_values = explainer(X_test)

# SHAP summary plot
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
plt.tight_layout()
plt.savefig(os.path.join(EVAL_DIR, "shap_summary.png"))
plt.close()

# ============================
# FEATURE IMPORTANCE
# ============================
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 6))
plt.bar(range(len(importances)), importances[indices], color='skyblue')
plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(EVAL_DIR, "feature_importance.png"))
plt.close()

# ============================
# ERROR ANALYSIS
# ============================
y_pred = model.predict(X_test)
errors = X_test[y_pred != y_test]

if len(errors) > 0:
    # Cluster errors if more than 1
    n_clusters = min(3, len(errors))
    if n_clusters > 1:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(errors)

    # Correlation heatmap of errors
    plt.figure(figsize=(10, 8))
    sns.heatmap(np.corrcoef(errors.T), cmap="coolwarm", annot=False)
    plt.title("Error Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(EVAL_DIR, "error_heatmap.png"))
    plt.close()

print("SHAP analysis, feature importance, and error analysis complete!")
print(f"Saved plots in: {EVAL_DIR}")
