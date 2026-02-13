import logging
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

from build_features import load_data, feature_engineering, build_pipeline

# Logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Correlation filter
def remove_correlated_features(X, feature_names, threshold=0.9):

    logger.info("Applying correlation threshold filter...")

    if hasattr(X, "toarray"):
        X = X.toarray()

    corr_matrix = np.corrcoef(X, rowvar=False)
    upper_triangle = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)

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

    # Correlation filtering
    X_corr, feature_names = remove_correlated_features(X_train, feature_names)

    # Mutual Information
    logger.info("Applying Mutual Information selection...")
    mi_scores = mutual_info_classif(X_corr, y_train)

    selected_indices = np.where(mi_scores > 0)[0]

    X_selected = X_corr[:, selected_indices]
    final_features = feature_names[selected_indices]

    logger.info(f"Final selected features: {len(final_features)}")

    # Save feature list
    os.makedirs("features", exist_ok=True)
    with open("features/feature_list.json", "w") as f:
        json.dump(list(final_features), f, indent=4)

    # Save arrays
    os.makedirs("data/processed", exist_ok=True)
    np.save("data/processed/X_train.npy", X_selected)
    np.save("data/processed/y_train.npy", y_train)

    X_test_selected = X_test[:, selected_indices]
    np.save("data/processed/X_test.npy", X_test_selected)
    np.save("data/processed/y_test.npy", y_test)

    # Plot feature importance
    os.makedirs("reports", exist_ok=True)

    sorted_idx = np.argsort(mi_scores[selected_indices])
    plt.figure()
    plt.barh(range(len(sorted_idx)), mi_scores[selected_indices][sorted_idx])
    plt.yticks(range(len(sorted_idx)), final_features[sorted_idx])
    plt.xlabel("Mutual Information Score")
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig("reports/feature_importance.png")
    plt.close()

    logger.info("Feature importance plot saved.")
    logger.info("Day-2 Feature Engineering + Selection Completed Successfully.")


if __name__ == "__main__":
    main()
