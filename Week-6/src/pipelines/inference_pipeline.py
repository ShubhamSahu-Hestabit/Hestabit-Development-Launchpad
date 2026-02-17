import os
import json
import joblib
import pandas as pd

from features.build_features import create_basic_features

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_lgbm_model.pkl")
FEATURE_LIST_PATH = os.path.join(BASE_DIR, "features", "feature_list.json")


class InferenceModel:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

        with open(FEATURE_LIST_PATH, "r") as f:
            self.selected_features = json.load(f)

    def preprocess(self, input_dict):

        # Convert input to DataFrame
        df = pd.DataFrame([input_dict])

        # Apply feature engineering (same as training)
        df = create_basic_features(df)

        # Drop target if accidentally created
        if "target" in df.columns:
            df = df.drop(columns=["target"])

        # Ensure all selected features exist
        for col in self.selected_features:
            if col not in df.columns:
                df[col] = 0

        # Ensure correct column order
        df = df[self.selected_features]

        return df  
    def predict(self, input_dict):

        X = self.preprocess(input_dict)

        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]

        return int(prediction), float(probability)
