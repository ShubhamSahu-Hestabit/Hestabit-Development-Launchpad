import logging
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

from build_features import load_data, feature_engineering, build_pipeline


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def to_dense(X):
    if hasattr(X, "toarray"):
        return X.toarray()
    return np.array(X)


def remove_correlated_features(X, feature_names, threshold=0.9):

    logger.info("Applying correlation threshold filter...")

    X = to_dense(X)

    corr_matrix = np.corrcoef(X, rowvar=False)

    to_drop = set()
    for i in range(corr_matrix.shape[0]):
        for j in range(i + 1, corr_matrix.shape[1]):
            if abs(corr_matrix[i, j]) > threshold:
                to_drop.add(j)

    keep_indices = [i for i in range(len(feature_names)) if i not in to_drop]

    X_filtered = X[:, keep_indices]
    feature_names_filtered = feature_names[keep_indices]

    logger.info(f"Features after correlation filter: {len(feature_names_filtered)}")

    return X_filtered, feature_names_filtered


def main():

    df = load_data()
    df = feature_engineering(df)

    X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)

    X_train = to_dense(X_train)
    X_test = to_dense(X_test)

    X_corr_train, feature_names_corr = remove_correlated_features(
        X_train,
        feature_names
    )

    X_corr_test = X_test[:, :X_corr_train.shape[1]]

    logger.info("Applying Mutual Information selection...")

    mi_scores = mutual_info_classif(X_corr_train, y_train, random_state=42)

    # -------- TOP-K SELECTION (Recommended) --------
    top_k = 10
    selected_indices = np.argsort(mi_scores)[-top_k:]

    # -------- THRESHOLD METHOD (Optional - Commented) --------
    # mi_threshold = 0.01
    # selected_indices = np.where(mi_scores >= mi_threshold)[0]
    # ----------------------------------------------------------

    X_selected_train = X_corr_train[:, selected_indices]
    X_selected_test = X_corr_test[:, selected_indices]

    final_features = feature_names_corr[selected_indices]

    logger.info(f"Top K selected features: {len(final_features)}")

    os.makedirs("features", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    with open("features/feature_list.json", "w") as f:
        json.dump(list(final_features), f, indent=4)

    np.save("data/processed/X_train.npy", X_selected_train)
    np.save("data/processed/X_test.npy", X_selected_test)
    np.save("data/processed/y_train.npy", y_train)
    np.save("data/processed/y_test.npy", y_test)

    X_full = np.concatenate([X_selected_train, X_selected_test], axis=0)
    y_full = np.concatenate([y_train, y_test], axis=0)

    np.save("data/processed/final_feature_matrix.npy", X_full)

    df_final = pd.DataFrame(X_full, columns=final_features)
    df_final["target"] = y_full
    df_final.to_csv("data/processed/final_feature_matrix.csv", index=False)

    logger.info("Saved final feature matrix (.npy and .csv)")

    sorted_idx = np.argsort(mi_scores[selected_indices])

    plt.figure()
    plt.barh(range(len(sorted_idx)),
             mi_scores[selected_indices][sorted_idx])
    plt.yticks(range(len(sorted_idx)),
               final_features[sorted_idx])
    plt.xlabel("Mutual Information Score")
    plt.title("Top 10 Feature Importance (MI)")
    plt.tight_layout()
    plt.savefig("reports/feature_importance.png")
    plt.close()

    logger.info("Feature importance plot saved.")
    logger.info("Feature Engineering + Selection Completed Successfully.")


if __name__ == "__main__":
    main()
