# Day-5 Capstone --- Model Deployment & MLOps Implementation

------------------------------------------------------------------------

# 1. Objective

Deploy a trained ML model into a production-ready system with:

-   API serving
-   Inference wrapper
-   Logging
-   Drift monitoring
-   Dashboard
-   Docker containerization

------------------------------------------------------------------------

# 2. Model Summary

## Algorithm

LightGBM (Gradient Boosted Trees)

## Training Pipeline

-   Feature engineering
-   Correlation filtering
-   Mutual Information selection
-   SMOTE balancing
-   Cross-validation
-   Optuna hyperparameter tuning

## Final Model Artifact

models/best_lgbm_model.pkl

Saved using:

``` python
joblib.dump(best_model, "best_lgbm_model.pkl")
```

------------------------------------------------------------------------

# 3. Inference Wrapper Architecture

File: src/pipelines/inference_pipeline.py

## Why We Built a Wrapper

Training and production environments differ. Directly loading a model
without consistent preprocessing can cause:

-   Feature mismatch
-   Encoding inconsistency
-   Training-serving skew
-   Silent production errors

## What the Wrapper Does

1.  Loads trained model
2.  Accepts raw user input
3.  Applies identical feature engineering logic
4.  Applies scaling/transformations
5.  Returns prediction and probability

This ensures safe and consistent inference.

------------------------------------------------------------------------

# 4. Alternative Production Approach

An alternative design is saving the full preprocessing + model pipeline:

``` python
full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", lgbm_model)
])

joblib.dump(full_pipeline, "full_pipeline.pkl")
```

Then in API:

``` python
pipeline.predict(raw_input)
```

We chose a manual wrapper for greater flexibility and control.

------------------------------------------------------------------------

# 5. API Layer (FastAPI)

File: src/deployement/api.py

## Endpoint

POST /predict

### Example Input

``` json
{
  "goal": 12000,
  "main_category": "Technology",
  "country": "US",
  "launched": "2017-03-01",
  "deadline": "2017-04-01"
}
```

### Response

``` json
{
  "request_id": "uuid",
  "model_version": "v1",
  "prediction": 1,
  "probability": 0.89
}
```

### Production Features

-   Input validation (Pydantic)
-   Unique Request ID
-   Timestamp tracking
-   Model versioning
-   CSV logging

------------------------------------------------------------------------

# 6. Prediction Logging

File: src/logs/prediction_logs.csv

Logs include: - Timestamp - Request ID - Input features - Prediction -
Probability

Used for monitoring, auditing, and drift detection.

------------------------------------------------------------------------

# 7. Drift Monitoring

File: src/monitoring/drift_checker.py

Functionality: - Reads prediction logs - Checks probability distribution
shift - Alerts if abnormal deviation detected

Run:

``` bash
python src/monitoring/drift_checker.py
```

------------------------------------------------------------------------

# 8. Dashboard (Streamlit)

File: src/dashboard/app.py

Displays: - Total predictions - Class distribution - Probability
histogram - Drift visualization

Run:

``` bash
streamlit run src/dashboard/app.py
```

------------------------------------------------------------------------

# 9. Docker Deployment

## LightGBM System Dependency

LightGBM requires: libgomp.so.1

Installed inside Docker using:

``` dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
```

------------------------------------------------------------------------

## Dockerfile Location

src/deployement/Dockerfile

## Build Command

``` bash
docker build -t kickstarter-ml -f src/deployement/Dockerfile .
```

## Run Command

``` bash
docker run -d -p 8000:8000 --name kickstarter_api kickstarter-ml
```

Access: http://localhost:8000/docs

------------------------------------------------------------------------

# 10. requirements.txt

    fastapi
    uvicorn
    pydantic
    pandas
    numpy
    scikit-learn
    lightgbm
    joblib
    python-dotenv
    streamlit
    matplotlib
    seaborn
    imblearn
    optuna

------------------------------------------------------------------------

# 11. Order of Execution

## Training Phase

1.  build_features.py
2.  feature_selector.py
3.  train.py
4.  tuning.py

## Deployment Phase (Local)

``` bash
uvicorn deployement.api:app --reload
```

## Docker Phase

``` bash
docker build -t kickstarter-ml -f src/deployement/Dockerfile .
docker run -d -p 8000:8000 --name kickstarter_api kickstarter-ml
```

------------------------------------------------------------------------

# 12. Screenshots

## Swagger UI

![Swagger UI](screenshots/swagger.png)

## Prediction Response

![Prediction Output](screenshots/predict.png)

## Dashboard View

![Dashboard](screenshots/dashboard_day5.png)

## Docker Running Container

![Docker Container](screenshots/docker.png)

------------------------------------------------------------------------

# 13. Final Conclusion

This capstone demonstrates:

-   End-to-end ML lifecycle
-   Safe inference architecture
-   Production API serving
-   Logging & monitoring
-   Drift detection
-   Docker containerization
-   System dependency handling
-   Real-world ML Engineering practices

