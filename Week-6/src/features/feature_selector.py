import logging
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif
from build_features import load_data, build_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def to_dense(X):
    return X.toarray() if hasattr(X, "toarray") else np.array(X)

def main():
    df = load_data()
    X_train, X_test, y_train, y_test, feature_names = build_pipeline(df)
    
    X_train = to_dense(X_train)
    X_test = to_dense(X_test)
    
    # Remove correlations
    logger.info("Removing highly correlated features...")
    corr_matrix = np.corrcoef(X_train, rowvar=False)
    to_drop = set()
    for i in range(corr_matrix.shape[0]):
        for j in range(i + 1, corr_matrix.shape[1]):
            if abs(corr_matrix[i, j]) > 0.85:
                to_drop.add(j)
    
    keep = [i for i in range(len(feature_names)) if i not in to_drop]
    X_train = X_train[:, keep]
    X_test = X_test[:, keep]
    feature_names = feature_names[keep]
    
    logger.info(f"After correlation filter: {len(feature_names)} features")
    
    # Mutual information
    logger.info("Selecting top features by mutual information...")
    mi_scores = mutual_info_classif(X_train, y_train, random_state=42)
    
    top_k = min(25, len(feature_names))
    selected = np.argsort(mi_scores)[-top_k:]
    
    X_train_final = X_train[:, selected]
    X_test_final = X_test[:, selected]
    final_features = feature_names[selected]
    
    logger.info(f"Selected {len(final_features)} features")
    
    # Save
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("features", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    np.save("data/processed/X_train.npy", X_train_final)
    np.save("data/processed/X_test.npy", X_test_final)
    np.save("data/processed/y_train.npy", y_train)
    np.save("data/processed/y_test.npy", y_test)
    
    with open("features/feature_list.json", "w") as f:
        json.dump(list(final_features), f, indent=4)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sorted_idx = np.argsort(mi_scores[selected])
    plt.barh(range(len(sorted_idx)), mi_scores[selected][sorted_idx])
    plt.yticks(range(len(sorted_idx)), final_features[sorted_idx], fontsize=8)
    plt.xlabel("Mutual Information")
    plt.title(f"Top {top_k} Features")
    plt.tight_layout()
    plt.savefig("reports/feature_importance.png", dpi=150)
    plt.close()
    
    logger.info("Done!")

if __name__ == "__main__":
    main()