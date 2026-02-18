import os
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCE_DATA = os.path.join(BASE_DIR, "data", "processed", "final.csv")
LOG_FILE = os.path.join(BASE_DIR, "..", "prediction_logs.csv")


def check_drift():

    if not os.path.exists(LOG_FILE):
        print("No predictions logged yet.")
        return

    reference_df = pd.read_csv(REFERENCE_DATA)
    production_df = pd.read_csv(LOG_FILE)

    numeric_cols = reference_df.select_dtypes(include=[np.number]).columns

    print("\n=== DATA DRIFT REPORT ===\n")

    for col in numeric_cols:
        if col in production_df.columns:
            stat, p_value = ks_2samp(
                reference_df[col].dropna(),
                production_df[col].dropna()
            )

            if p_value < 0.05:
                print(f"Drift detected in: {col}")
