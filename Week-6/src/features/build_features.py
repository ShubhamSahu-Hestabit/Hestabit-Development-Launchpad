import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def load_data():
    df = pd.read_csv("/home/shubhamsahu/Hestabit-Development Launchpad/Week-6/src/data/processed/final.csv")
    logger.info(f"Loaded data: {df.shape}")
    return df

def create_basic_features(df):
    """Create features that DON'T require target information"""
    df = df.copy()
    
    # Target
    df["target"] = (df["state"] == "successful").astype(int)
    
    # Remove leakage
    drop = ["state", "pledged", "usd pledged", "usd_pledged_real", "backers", "ID", "name"]
    df = df.drop(columns=[c for c in drop if c in df.columns])
    
    # Dates
    df["launched"] = pd.to_datetime(df["launched"])
    df["deadline"] = pd.to_datetime(df["deadline"])
    df["campaign_duration"] = (df["deadline"] - df["launched"]).dt.days
    df["launch_month"] = df["launched"].dt.month
    df["launch_weekday"] = df["launched"].dt.weekday
    df["launch_year"] = df["launched"].dt.year
    
    # Flags
    df["is_weekend"] = df["launch_weekday"].isin([5, 6]).astype(int)
    df["is_short"] = (df["campaign_duration"] < 30).astype(int)
    
    # Goal
    df["goal_log"] = np.log1p(df["goal"])
    df["goal_per_day"] = df["goal"] / (df["campaign_duration"] + 1)
    df["high_goal_short"] = ((df["goal"] > df["goal"].median()) & (df["campaign_duration"] < 30)).astype(int)
    
    # Cyclical
    df["month_sin"] = np.sin(2 * np.pi * df["launch_month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["launch_month"] / 12)
    
    df = df.drop(columns=["launched", "deadline"])
    
    return df

def build_pipeline(df):
    """
    Build pipeline with ZERO leakage.
    Target encoding happens AFTER split!
    """
    df = create_basic_features(df)
    
    X = df.drop(columns=["target"])
    y = df["target"]
    
    # SPLIT FIRST
    logger.info("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # NOW add target-encoded features (NO LEAKAGE!)
    logger.info("Adding target-encoded features (train only)...")
    
    if "main_category" in X_train.columns:
        cat_rates = X_train.assign(target=y_train).groupby("main_category")["target"].mean()
        X_train["cat_rate"] = X_train["main_category"].map(cat_rates).fillna(y_train.mean())
        X_test["cat_rate"] = X_test["main_category"].map(cat_rates).fillna(y_train.mean())
    
    if "country" in X_train.columns:
        country_rates = X_train.assign(target=y_train).groupby("country")["target"].mean()
        X_train["country_rate"] = X_train["country"].map(country_rates).fillna(y_train.mean())
        X_test["country_rate"] = X_test["country"].map(country_rates).fillna(y_train.mean())
    
    # Preprocessing
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns.tolist()
    
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
    ])
    
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    logger.info(f"Final: Train {X_train_processed.shape}, Test {X_test_processed.shape}")
    
    return X_train_processed, X_test_processed, y_train.values, y_test.values, preprocessor.get_feature_names_out()