import os
import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from pipelines.inference_pipeline import InferenceModel

app = FastAPI(title="Kickstarter Prediction API")

model = InferenceModel()

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "prediction_logs.csv")
os.makedirs(LOG_DIR, exist_ok=True)


class PredictionRequest(BaseModel):
    goal: float
    main_category: str
    country: str
    launched: str
    deadline: str


@app.post("/predict")
def predict(request: PredictionRequest):

    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    input_data = request.dict()

    prediction, probability = model.predict(input_data)

    log_entry = {
        "request_id": request_id,
        "timestamp": timestamp,
        "prediction": prediction,
        "probability": probability
    }

    df = pd.DataFrame([log_entry])

    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)

    return {
        "request_id": request_id,
        "model_version": "v1",
        "prediction": prediction,
        "probability": probability
    }
