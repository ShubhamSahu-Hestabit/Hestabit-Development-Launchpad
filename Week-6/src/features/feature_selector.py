# src/features/feature_selector.py

import os
import joblib
import logging
import numpy as np

from sklearn.feature_selection import mutual_info_classif

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================
# PATHS
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

os.makedirs(ARTIFACT_DIR, exist_ok=True)


# ============================
# FEATURE SELECTOR CLASS
# ============================

class FeatureSelector:

    def __init__(self):
        self.corr_keep_indices = None
        self.mi_selected_indices = None

    def fit(self, X_train, y_train):

        if hasattr(X_train, "toarray"):
            X_train = X_train.toarray()

        # Correlation filter
        logger.info("Applying correlation filtering...")

        corr_matrix = np.corrcoef(X_train, rowvar=False)
        to_drop = set()

        for i in range(corr_matrix.shape[0]):
            for j in range(i + 1, corr_matrix.shape[1]):
                if abs(corr_matrix[i, j]) > 0.85:
                    to_drop.add(j)

        self.corr_keep_indices = [
            i for i in range(X_train.shape[1]) if i not in to_drop
        ]

        X_filtered = X_train[:, self.corr_keep_indices]

        # Mutual Information
        logger.info("Selecting top features using Mutual Information...")

        mi_scores = mutual_info_classif(X_filtered, y_train, random_state=42)

        top_k = min(25, X_filtered.shape[1])
        self.mi_selected_indices = np.argsort(mi_scores)[-top_k:]

        return self

    def transform(self, X):

        if hasattr(X, "toarray"):
            X = X.toarray()

        X = X[:, self.corr_keep_indices]
        X = X[:, self.mi_selected_indices]

        return X


# ============================
# MAIN
# ============================

def main():

    X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
    X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
    y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))
    y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

    selector = FeatureSelector()
    selector.fit(X_train, y_train)

    X_train_final = selector.transform(X_train)
    X_test_final = selector.transform(X_test)

    # Save final arrays
    np.save(os.path.join(DATA_DIR, "X_train.npy"), X_train_final)
    np.save(os.path.join(DATA_DIR, "X_test.npy"), X_test_final)

    # Save selector object
    joblib.dump(selector, os.path.join(ARTIFACT_DIR, "feature_selector.pkl"))
    logger.info("Saved feature_selector.pkl")

    logger.info("Feature selection completed successfully.")


if __name__ == "__main__":
    main()
