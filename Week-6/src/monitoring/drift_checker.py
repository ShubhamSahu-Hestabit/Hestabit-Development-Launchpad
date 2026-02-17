import os
import pandas as pd

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "prediction_logs.csv")

def check_drift():

    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return

    df = pd.read_csv(LOG_FILE)

    if len(df) < 5:
        print("Not enough predictions.")
        return

    mean_prob = df["probability"].mean()

    print(f"Mean Probability: {mean_prob:.4f}")

    if mean_prob > 0.9 or mean_prob < 0.1:
        print("[ALERT] Possible Drift!")
    else:
        print("Model Stable.")

if __name__ == "__main__":
    check_drift()
