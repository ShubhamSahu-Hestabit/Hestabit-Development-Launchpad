# Week 6 - End-to-End Machine Learning Pipeline

This week focuses on building a complete machine learning pipeline step by step, covering data analysis, feature engineering, model training, evaluation, interpretation, and deployment.

---

## Folder Structure

```
Week-6/
├── Day-1/
│   ├── images/
│   ├── src/
│   │   ├── data/processed/
│   │   │   └── final.csv
│   │   ├── notebooks/
│   │   │   ├── EDA_final.ipynb
│   │   │   └── EDA_raw.ipynb
│   │   └── pipelines/
│   ├── DATA-REPORT.md
│   └── Day-1 Data Numbers.csv
├── Day-2/
│   ├── images/
│   ├── src/features/
│   │   ├── build_features.py
│   │   ├── feature_list.json
│   │   └── feature_selector.py
│   ├── FEATURE-ENGINEERING-REPORT.md
│   └── DAY-2 Feature Engineering Summary.csv
├── Day-3/
│   ├── images/
│   ├── src/
│   │   ├── evaluation/
│   │   │   └── metrics.json
│   │   ├── models/
│   │   │   └── best_model.pkl
│   │   └── training/
│   │       └── train.py
│   ├── MODEL-COMPARISON.md
│   └── model_stability_metrics.csv
├── Day-4/
│   ├── images/
│   ├── src/
│   │   ├── evaluation/
│   │   │   └── shap_analysis.py
│   │   └── training/
│   │       └── tuning.py
│   ├── tuning/
│   │   └── results.json
│   └── MODEL-INTERPRETATION.md
├── Day-5/
│   ├── screenshots/
│   ├── src/
│   │   ├── deployment/
│   │   │   ├── api.py
│   │   │   └── Dockerfile
│   │   └── monitoring/
│   │       └── drift_checker.py
│   ├── DEPLOYMENT-NOTES.md
│   └── prediction_logs.csv
├── src/
│   ├── artifacts/
│   ├── dashboard/
│   ├── data/
│   │   ├── processed/
│   │   └── raw/
│   ├── deployment/
│   ├── evaluation/
│   ├── features/
│   ├── logs/
│   ├── models/
│   ├── monitoring/
│   ├── notebooks/
│   ├── pipelines/
│   ├── reports/
│   ├── training/
│   └── tuning/
├── requirements.txt
└── README.md
```

---

## Day-wise Work

- Day-1: Data Analysis  
  Includes two EDA deliverables:
  - EDA on raw dataset (EDA_raw.ipynb)
  - EDA on processed dataset (EDA_final.ipynb)

- Day-2: Feature Engineering  
  Feature building, selection, and transformation logic

- Day-3: Model Training and Evaluation  
  Model training pipeline, evaluation metrics, and comparison

- Day-4: Model Interpretation and Tuning  
  SHAP analysis and hyperparameter tuning

- Day-5: Deployment and Monitoring  
  API creation, Docker setup, and data drift monitoring

---

## Main src Folder (Final Pipeline)

The src folder contains the final integrated machine learning pipeline:

- data processing and storage  
- feature engineering pipeline  
- model training and evaluation  
- model tuning and interpretation  
- deployment and inference  
- monitoring and logging  
