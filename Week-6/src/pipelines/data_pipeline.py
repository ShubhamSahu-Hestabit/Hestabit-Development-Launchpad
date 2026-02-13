import logging
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "data_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

RAW_PATH = BASE_DIR / "data" / "raw" / "kickstarter_30k.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "final.csv"


def load_data(path: Path) -> pd.DataFrame:
    logger.info("Loading raw dataset")
    df = pd.read_csv(path)
    logger.info(f"Dataset shape: {df.shape}")
    return df


def log_dataset_info(df: pd.DataFrame):
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"Data types:\n{df.dtypes}")

    missing = df.isnull().sum()
    logger.info(f"Missing values per column:\n{missing}")

    duplicates = df.duplicated().sum()
    logger.info(f"Duplicate rows: {duplicates}")

    if "target" in df.columns:
        logger.info(
            f"Target distribution:\n{df['target'].value_counts(normalize=True)}"
        )


def remove_leakage_columns(df: pd.DataFrame) -> pd.DataFrame:
    leakage_cols = ["pledged", "backers", "usd pledged", "usd_pledged_real"]
    cols_to_drop = [col for col in leakage_cols if col in df.columns]

    df = df.drop(columns=cols_to_drop)
    logger.info(f"Removed leakage columns: {cols_to_drop}")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]

    logger.info(f"Removed duplicate rows: {before - after}")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(exclude=np.number).columns

    for col in numeric_cols:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
        logger.info(f"Filled missing numeric column '{col}' with median: {median_value}")

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")
        logger.info(f"Filled missing categorical column '{col}' with 'Unknown'")

    logger.info("Missing value handling completed")
    return df


def cap_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers_before = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]

        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        logger.info(
            f"IQR applied on '{col}' | "
            f"Lower: {lower_bound:.2f}, Upper: {upper_bound:.2f}, "
            f"Outliers capped: {outliers_before}"
        )

    logger.info("Outlier capping completed")
    return df


def save_data(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Cleaned dataset saved at: {path}")


def main():
    logger.info("Data pipeline started")

    df = load_data(RAW_PATH)
    log_dataset_info(df)

    df = remove_leakage_columns(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = cap_outliers_iqr(df)

    save_data(df, PROCESSED_PATH)

    logger.info("Data pipeline completed successfully")


if __name__ == "__main__":
    main()
