# /evaluation/shap_analysis.py

import os
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix

# -------- LOAD DATA --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "features", "data", "processed")
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")

X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

model = joblib.load(MODEL_PATH)

# -------- SHAP --------
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)

plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig(os.path.join(EVAL_DIR, "shap_summary.png"))
plt.close()

# -------- FEATURE IMPORTANCE --------
importances = model.feature_importances_
plt.figure()
plt.bar(range(len(importances)), importances)
plt.title("Feature Importance")
plt.savefig(os.path.join(EVAL_DIR, "feature_importance.png"))
plt.close()

# -------- ERROR ANALYSIS --------
y_pred = model.predict(X_test)

errors = X_test[y_pred != y_test]

if len(errors) > 10:
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(errors)

    plt.figure()
    sns.heatmap(np.corrcoef(errors.T), cmap="coolwarm")
    plt.title("Error Correlation Heatmap")
    plt.savefig(os.path.join(EVAL_DIR, "error_heatmap.png"))
    plt.close()

print("SHAP and error analysis complete.")
