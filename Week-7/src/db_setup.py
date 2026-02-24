import os
import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

CSV_PATH = os.path.join(DATA_DIR, "products.csv")
DB_PATH = os.path.join(DATA_DIR, "enterprise.db")


def setup_database():
    df = pd.read_csv(CSV_PATH)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df.to_sql("products", engine, if_exists="replace", index=False)
    print("Database created successfully.")


if __name__ == "__main__":
    setup_database()