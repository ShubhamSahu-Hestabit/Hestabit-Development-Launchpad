import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_PATH = "/home/shubhamsahu/Hestabit-Development Launchpad/Week-6/src/data/processed/final.csv"


# Load dataset
def load_data():
    logger.info("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    logger.info(f"Dataset shape: {df.shape}")
    return df


# Feature engineering
def feature_engineering(df):

    logger.info("Removing leakage columns...")
    leakage_cols = ["pledged", "usd pledged", "usd_pledged_real", "backers"]
    df = df.drop(columns=[col for col in leakage_cols if col in df.columns])

    logger.info("Converting date columns...")
    df["launched"] = pd.to_datetime(df["launched"])
    df["deadline"] = pd.to_datetime(df["deadline"])

    logger.info("Creating engineered features...")

    # Duration
    df["campaign_duration"] = (df["deadline"] - df["launched"]).dt.days

    # Date features
    df["launch_year"] = df["launched"].dt.year
    df["launch_month"] = df["launched"].dt.month
    df["launch_day"] = df["launched"].dt.day
    df["launch_weekday"] = df["launched"].dt.weekday
    df["is_weekend_launch"] = df["launch_weekday"].isin([5, 6]).astype(int)

    # Goal transformations
    df["goal_log"] = np.log1p(df["usd_goal_real"])
    df["goal_sqrt"] = np.sqrt(df["usd_goal_real"])

    # Goal bucket
    df["goal_bucket"] = pd.qcut(
        df["usd_goal_real"],
        q=3,
        labels=["low", "medium", "high"]
    )

    # Name-based features
    df["name_length"] = df["name"].astype(str).apply(len)
    df["name_word_count"] = df["name"].astype(str).apply(lambda x: len(x.split()))
    df["has_number_in_name"] = df["name"].astype(str).str.contains(r"\d").astype(int)

    df = df.drop(columns=["launched", "deadline", "name"])

    return df


# Build preprocessing pipeline
def build_pipeline(df):

    logger.info("Splitting train/test...")
    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns
    numerical_cols = X_train.select_dtypes(include=["int64", "float64"]).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    logger.info("Fitting preprocessing pipeline...")
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    feature_names = preprocessor.get_feature_names_out()

    logger.info(f"Total features after encoding: {len(feature_names)}")

    return X_train_processed, X_test_processed, y_train, y_test, feature_names
