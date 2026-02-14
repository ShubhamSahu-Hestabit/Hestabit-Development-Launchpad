import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_data():

    logger.info("Loading dataset...")

    df = pd.read_csv(
        "/home/shubhamsahu/Hestabit-Development Launchpad/Week-6/src/data/processed/final.csv"
    )

    logger.info(f"Dataset shape: {df.shape}")

    return df


def feature_engineering(df):

    logger.info("Removing high-cardinality columns...")

    for col in ["ID", "name"]:
        if col in df.columns:
            df = df.drop(columns=col)

    logger.info("Creating target variable...")

    df["target"] = (df["state"] == "successful").astype(int)

    logger.info("Removing leakage columns...")

    leakage_cols = [
        "state",
        "pledged",
        "usd pledged",
        "usd_pledged_real",
        "backers"
    ]

    for col in leakage_cols:
        if col in df.columns:
            df = df.drop(columns=col)

    logger.info("Creating date features...")

    df["launched"] = pd.to_datetime(df["launched"])
    df["deadline"] = pd.to_datetime(df["deadline"])

    df["campaign_duration"] = (
        df["deadline"] - df["launched"]
    ).dt.days

    df["launch_month"] = df["launched"].dt.month
    df["launch_weekday"] = df["launched"].dt.weekday
    df["is_weekend_launch"] = df["launch_weekday"].isin([5, 6]).astype(int)

    logger.info("Creating goal transformations...")

    df["goal_log"] = np.log1p(df["goal"])

    df["goal_bucket"] = pd.qcut(
        df["goal"],
        q=3,
        labels=["low", "medium", "high"]
    )

    df = df.drop(columns=["launched", "deadline"])

    return df


def build_pipeline(df):

    logger.info("Splitting train/test...")

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    numeric_cols = X_train.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns

    numeric_pipeline = Pipeline([
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ])

    logger.info("Fitting preprocessing pipeline...")

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    feature_names = preprocessor.get_feature_names_out()

    logger.info(f"Total features after encoding: {len(feature_names)}")

    return (
        X_train_processed,
        X_test_processed,
        y_train.values,
        y_test.values,
        feature_names
    )
