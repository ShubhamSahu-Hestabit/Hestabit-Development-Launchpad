import os
import joblib
import uuid
import pandas as pd
from datetime import datetime


class InferenceEngine:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.preprocessor = joblib.load(
            os.path.join(BASE_DIR, "artifacts", "preprocessor.pkl")
        )

        self.selector = joblib.load(
            os.path.join(BASE_DIR, "artifacts", "feature_selector.pkl")
        )

        self.model = joblib.load(
            os.path.join(BASE_DIR, "models", "best_lgbm_model.pkl")
        )

        self.model_version = "v1.0.0"

    def predict(self, input_dict):

        request_id = str(uuid.uuid4())

        df = pd.DataFrame([input_dict])

        # 1️⃣ Preprocessing (feature engineering + encoding + scaling)
        X = self.preprocessor.transform(df)

        # 2️⃣ Feature selection
        X = self.selector.transform(X)

        # 3️⃣ Model prediction
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]

        result = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "model_version": self.model_version,
            "prediction": int(prediction),
            "probability": float(probability)
        }

        self.log_prediction(input_dict, result)

        return result

    def log_prediction(self, input_data, result):

        log_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prediction_logs.csv"
        )

        log_entry = {**input_data, **result}
        df = pd.DataFrame([log_entry])

        if not os.path.exists(log_file):
            df.to_csv(log_file, index=False)
        else:
            df.to_csv(log_file, mode="a", header=False, index=False)
