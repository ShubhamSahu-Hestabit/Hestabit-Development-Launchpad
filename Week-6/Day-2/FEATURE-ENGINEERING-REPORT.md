# DAY-2 --- Feature Engineering & Selection Report

## Objective

Dataset Size: 30,000 rows

------------------------------------------------------------------------

# 1️⃣ Data Cleaning & Leakage Removal

## Target Creation

target = 1 if state == "successful" else 0

## Leakage Columns Removed

  Column Name        Reason
  ------------------ ----------------------------
  state              Directly determines target
  pledged            Known after campaign ends
  usd pledged        Known after campaign ends
  usd_pledged_real   Known after campaign ends
  backers            Known after campaign ends

------------------------------------------------------------------------

# 2️⃣ High Cardinality Feature Removal

  Column   Reason
  -------- --------------------------------------------------
  ID       Identifier, no predictive value
  name     Extremely high cardinality (\~30k unique values)

------------------------------------------------------------------------

# 3️⃣ Feature Engineering

## Date-Based Features

  Feature             Description
  ------------------- ----------------------------------
  campaign_duration   Days between launch and deadline
  launch_month        Launch month
  launch_weekday      Launch weekday
  is_weekend_launch   Weekend launch indicator

## Goal Transformations

  Feature       Description
  ------------- ---------------------------------------
  goal_log      Log-transformed funding goal
  goal_bucket   Low / Medium / High goal segmentation

------------------------------------------------------------------------

# 4️⃣ Preprocessing & Encoding

  Feature Type   Method Used
  -------------- -----------------------------------------
  Numerical      StandardScaler
  Categorical    OneHotEncoder (handle_unknown="ignore")
  Framework      ColumnTransformer

------------------------------------------------------------------------

# Feature Count Summary

  Stage                                      Feature Count
  ------------------------------------------ ---------------
  After Encoding                             225
  After Correlation Filter (0.9 threshold)   208
  After Mutual Information (Top-10)          10

------------------------------------------------------------------------

# 5️⃣ Feature Selection Strategy

## Step 1 --- Correlation Filtering

-   Threshold: 0.9
-   Removes redundant highly correlated features

## Step 2 --- Mutual Information Selection

Final strategy used:

Top 10 features based on Mutual Information score

------------------------------------------------------------------------

# 6️⃣ Final Selected Features (Example)

  Selected Feature
  -----------------------------
  num\_\_goal
  num\_\_goal_log
  num\_\_campaign_duration
  cat\_\_goal_bucket_low
  cat\_\_goal_bucket_medium
  cat\_\_goal_bucket_high
  cat\_\_category_Fiction
  cat\_\_category_Blues
  cat\_\_category_Woodworking
  cat\_\_main_category_Music

------------------------------------------------------------------------
![Day-2 Feature Engineering Summary](images/importance.png)


# 7️⃣ Saved Artifacts

  File                         Purpose
  ---------------------------- ------------------------------
  features/feature_list.json   Final selected feature names
  X_train.npy / X_test.npy     Training & testing matrices
  y_train.npy / y_test.npy     Labels
  final_feature_matrix.npy     Combined matrix
  final_feature_matrix.csv     CSV version
  feature_importance.png       MI importance plot

------------------------------------------------------------------------


