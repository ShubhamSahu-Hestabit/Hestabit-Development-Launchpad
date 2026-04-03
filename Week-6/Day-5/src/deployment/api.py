import os
import sys
import types
import uuid
import joblib
import logging
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

# ============================
# 🔥 CRITICAL PICKLE FIX
# ============================

# Import original classes
from features.build_features import FeatureBuilder
from features.feature_selector import FeatureSelector

# Create fake __main__ module so pickle can resolve classes
main_module = types.ModuleType("__main__")
main_module.FeatureBuilder = FeatureBuilder
main_module.FeatureSelector = FeatureSelector

sys.modules["__main__"] = main_module


# ============================
# CONFIG
# ============================

MODEL_VERSION = "v1.0"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_DIR = os.path.join(BASE_DIR, "models")
LOG_FILE = os.path.join(BASE_DIR, "prediction_logs.csv")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Kickstarter Success Prediction API")


# ============================
# LOAD ARTIFACTS (ON STARTUP)
# ============================

@app.on_event("startup")
def load_artifacts():
    global feature_builder, preprocessor, selector, model

    try:
        logger.info("Loading model artifacts...")

        feature_builder = joblib.load(
            os.path.join(ARTIFACT_DIR, "feature_builder.pkl")
        )
        preprocessor = joblib.load(
            os.path.join(ARTIFACT_DIR, "preprocessor.pkl")
        )
        selector = joblib.load(
            os.path.join(ARTIFACT_DIR, "feature_selector.pkl")
        )
        model = joblib.load(
            os.path.join(MODEL_DIR, "best_lgbm_model.pkl")
        )

        logger.info("Artifacts loaded successfully.")

    except Exception as e:
        logger.error(f"Failed to load artifacts: {e}")
        raise e


# ============================
# INPUT SCHEMA
# ============================

class CampaignInput(BaseModel):
    category: str
    main_category: str
    currency: str
    deadline: str
    goal: float
    launched: str
    country: str
    usd_goal_real: float

    @field_validator("deadline", "launched")
    @classmethod
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return value


# ============================
# HEALTH CHECK
# ============================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_version": MODEL_VERSION
    }


# ============================
# PREDICT ENDPOINT
# ============================

@app.post("/predict")
def predict(data: CampaignInput):

    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    try:
        input_df = pd.DataFrame([data.model_dump()])

        # 1️⃣ Feature Engineering
        X_transformed = feature_builder.transform(input_df)

        # 2️⃣ Preprocessing
        X_processed = preprocessor.transform(X_transformed)

        # 3️⃣ Feature Selection
        X_selected = selector.transform(X_processed)

        # 4️⃣ Model Prediction
        prediction = model.predict(X_selected)[0]
        probability = model.predict_proba(X_selected)[0][1]

        result = {
            "request_id": request_id,
            "model_version": MODEL_VERSION,
            "prediction": int(prediction),
            "probability_success": float(round(probability, 4))
        }

        log_prediction(
            request_id=request_id,
            timestamp=timestamp,
            inputs=data.model_dump(),
            prediction=prediction,
            probability=probability
        )

        return result

    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================
# LOGGING FUNCTION
# ============================

def log_prediction(request_id, timestamp, inputs, prediction, probability):

    log_data = {
        "request_id": request_id,
        "timestamp": timestamp,
        "model_version": MODEL_VERSION,
        "prediction": int(prediction),
        "probability": float(probability),
        **inputs
    }

    df = pd.DataFrame([log_data])

    try:
        if not os.path.exists(LOG_FILE):
            df.to_csv(LOG_FILE, index=False)
        else:
            df.to_csv(LOG_FILE, mode="a", header=False, index=False)

    except Exception as e:
        logger.error(f"Logging failed: {e}")
