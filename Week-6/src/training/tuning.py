import os
import json
import joblib
import optuna
import numpy as np

from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "features", "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
TUNING_DIR = os.path.join(BASE_DIR, "tuning")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(TUNING_DIR, exist_ok=True)

X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))

neg, pos = np.bincount(y_train)
scale_pos_weight = neg / pos if pos != 0 else 1

print("Feature count:", X_train.shape[1])
print("Class distribution:", np.bincount(y_train))


def objective(trial):

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 400, 1200),
        "max_depth": trial.suggest_int("max_depth", 3, 7),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08),
        "subsample": trial.suggest_float("subsample", 0.7, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.7, 1.0),
        "gamma": trial.suggest_float("gamma", 0, 2),
        "reg_alpha": trial.suggest_float("reg_alpha", 0, 5),
        "reg_lambda": trial.suggest_float("reg_lambda", 1, 8),
        "scale_pos_weight": scale_pos_weight,
        "eval_metric": "logloss",
        "random_state": 42,
        "n_jobs": -1
    }

    model = XGBClassifier(**params)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []

    for train_idx, val_idx in cv.split(X_train, y_train):
        X_tr, X_val = X_train[train_idx], X_train[val_idx]
        y_tr, y_val = y_train[train_idx], y_train[val_idx]

        model.fit(X_tr, y_tr)
        y_prob = model.predict_proba(X_val)[:, 1]
        scores.append(roc_auc_score(y_val, y_prob))

    return np.mean(scores)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

print("Best ROC-AUC:", study.best_value)
print("Best Params:", study.best_params)

best_model = XGBClassifier(
    **study.best_params,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

best_model.fit(X_train, y_train)
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))

with open(os.path.join(TUNING_DIR, "results.json"), "w") as f:
    json.dump({
        "best_cv_roc_auc": study.best_value,
        "best_params": study.best_params,
        "feature_count": X_train.shape[1]
    }, f, indent=4)

print("Tuning complete. Model saved.")
