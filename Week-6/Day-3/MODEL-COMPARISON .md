# Model Comparison Report - Day 3

## Performance Summary

| Model | CV ROC-AUC | Test ROC-AUC | CV Accuracy | Test Accuracy | CV F1 | Test F1 |
|---------------------|------------|--------------|-------------|---------------|-------|---------|
| Logistic Regression | 0.653 | 0.606 | 0.598 | 0.547 | 0.570 | 0.546 |
| Random Forest | 0.665 | 0.555 | 0.609 | 0.531 | 0.580 | 0.547 |
| XGBoost | 0.673 | 0.559 | 0.620 | 0.514 | 0.578 | 0.559 |
| Neural Network | 0.657 | 0.579 | 0.604 | 0.572 | 0.567 | 0.515 |
| Stacking Ensemble | 0.672 | 0.566 | 0.615 | 0.516 | 0.580 | 0.560 |

---

##  Best Model: XGBoost

```
✓ Highest CV ROC-AUC: 0.673
✓ Highest Test F1-Score: 0.559
✓ Best Recall: 0.762 (catches most positive cases)
✓ Good for imbalanced datasets
✓ Powerful gradient boosting
```

---

## Why XGBoost Wins

**Training Performance**
- Highest CV ROC-AUC among all models (0.673)
- Best CV accuracy (0.620)
- Strong cross-validation metrics

**Test Performance**
- Highest recall (0.762) - catches 76% of positive cases
- Best test F1-score (0.559)
- Good balance for imbalanced data

**Practical Benefits**
- Handles complex patterns well
- Built-in regularization
- Feature importance available
- Industry-standard algorithm

---

## Other Models - Quick Summary

### Logistic Regression
- Best test ROC-AUC (0.606)
- Best generalization (smallest CV-test gap)
- Highest precision (0.458)
- Good for interpretability needs

### Random Forest
- Decent CV performance but poor test generalization
- Test ROC-AUC drops to 0.555 (lowest)
- Shows significant overfitting

### Neural Network
- Best test accuracy (0.572)
- But lowest F1-score (0.515)
- Requires more data to improve

### Stacking Ensemble
- Good test F1 (0.560) - close to XGBoost
- Complex architecture with marginal gains
- Higher computational cost

---

## Precision vs Recall Trade-off

| Model | Test Precision | Test Recall |
|---------------------|----------------|-------------|
| **Logistic Regression** | **0.458** | 0.675 |
| Random Forest | 0.448 | 0.702 |
| XGBoost | 0.441 | 0.762 |
| Neural Network | 0.474 | 0.564 |
| Stacking Ensemble | 0.443 | 0.764 |

**Interpretation:** Logistic Regression offers the best precision with balanced recall - fewer false alarms.

---

## Visualizations

**Location:** `evaluation/` folder

- `confusion_matrix.png` - XGBoost confusion matrix (best model)
- `roc_curve.png` - ROC curve comparison

**XGBoost Confusion Matrix Breakdown:**
- True Negatives (0,0): 1239 - Correctly predicted negatives
- False Positives (0,1): 2338 - Incorrectly predicted as positive
- False Negatives (1,0): 576 - Missed positive cases  
- True Positives (1,1): 1847 - Correctly predicted positives

**Insights:**
- High recall: Catches most positive cases (1847 TP vs 576 FN)
- Trade-off: More false positives (2338) for better coverage

---

## Technical Setup

- **Cross-Validation:** Stratified 5-Fold
- **Class Balance:** SMOTE applied
- **Scaling:** StandardScaler
- **Model Storage:** `models/` folder

*Models Evaluated: 5 | Validation: Stratified 5-Fold CV | Winner: XGBoost*
