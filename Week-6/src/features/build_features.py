# src/features/build_features.py

import os
import joblib
import logging
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# ============================
# PATHS
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "final.csv")
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

os.makedirs(ARTIFACT_DIR, exist_ok=True)


# ============================
# FEATURE BUILDER CLASS
# ============================

class FeatureBuilder:

    def __init__(self):
        self.cat_mapping = None
        self.country_mapping = None
        self.global_mean = None

    def create_basic_features(self, df):

        df = df.copy()

        if "state" in df.columns:
            df["target"] = (df["state"] == "successful").astype(int)

        drop_cols = [
            "state", "pledged", "usd pledged",
            "usd_pledged_real", "backers",
            "ID", "name"
        ]
        df = df.drop(columns=[c for c in drop_cols if c in df.columns])

        df["launched"] = pd.to_datetime(df["launched"])
        df["deadline"] = pd.to_datetime(df["deadline"])

        df["campaign_duration"] = (df["deadline"] - df["launched"]).dt.days
        df["launch_month"] = df["launched"].dt.month
        df["launch_weekday"] = df["launched"].dt.weekday
        df["launch_year"] = df["launched"].dt.year

        df["is_weekend"] = df["launch_weekday"].isin([5, 6]).astype(int)
        df["is_short"] = (df["campaign_duration"] < 30).astype(int)

        df["goal_log"] = np.log1p(df["goal"])
        df["goal_per_day"] = df["goal"] / (df["campaign_duration"] + 1)

        median_goal = df["goal"].median()
        df["high_goal_short"] = (
            (df["goal"] > median_goal) &
            (df["campaign_duration"] < 30)
        ).astype(int)

        df["month_sin"] = np.sin(2 * np.pi * df["launch_month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["launch_month"] / 12)

        df = df.drop(columns=["launched", "deadline"])

        return df

    def fit(self, df):

        df = self.create_basic_features(df)

        X = df.drop(columns=["target"])
        y = df["target"]

        self.global_mean = y.mean()

        self.cat_mapping = (
            X.assign(target=y)
            .groupby("main_category")["target"]
            .mean()
            .to_dict()
        )

        self.country_mapping = (
            X.assign(target=y)
            .groupby("country")["target"]
            .mean()
            .to_dict()
        )

        return self

    def transform(self, df):

        df = self.create_basic_features(df)

        df["cat_rate"] = df["main_category"].map(self.cat_mapping).fillna(self.global_mean)
        df["country_rate"] = df["country"].map(self.country_mapping).fillna(self.global_mean)

        if "target" in df.columns:
            X = df.drop(columns=["target"])
            y = df["target"]
            return X, y

        return df


# ============================
# BUILD PIPELINE
# ============================

def build_pipeline(df):

    feature_builder = FeatureBuilder()
    feature_builder.fit(df)

    joblib.dump(feature_builder, os.path.join(ARTIFACT_DIR, "feature_builder.pkl"))
    logger.info("Saved feature_builder.pkl")

    X, y = feature_builder.transform(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X_train.select_dtypes(include=["object"]).columns.tolist()

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
    ])

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    joblib.dump(preprocessor, os.path.join(ARTIFACT_DIR, "preprocessor.pkl"))
    logger.info("Saved preprocessor.pkl")

    return X_train_processed, X_test_processed, y_train.values, y_test.values


# ============================
# MAIN
# ============================

def main():

    df = pd.read_csv(DATA_PATH)

    X_train, X_test, y_train, y_test = build_pipeline(df)

    np.save(os.path.join(BASE_DIR, "data", "processed", "X_train.npy"), X_train)
    np.save(os.path.join(BASE_DIR, "data", "processed", "X_test.npy"), X_test)
    np.save(os.path.join(BASE_DIR, "data", "processed", "y_train.npy"), y_train)
    np.save(os.path.join(BASE_DIR, "data", "processed", "y_test.npy"), y_test)

    logger.info("Build stage completed successfully.")


if __name__ == "__main__":
    main()
