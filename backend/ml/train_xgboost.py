import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)

from xgboost import XGBClassifier

# -------------------------------------------------
# 1. Load engineered dataset
# -------------------------------------------------
DATA_PATH = "backend/data/clean_ml_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

#X = df.drop(columns=["eligible"])
X = df.drop(columns=["eligible","egrantz_eligible"])
y = df["eligible"]
# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)
# 3. Train XGBoost Model
xgb = XGBClassifier(n_estimators=300,max_depth=4,learning_rate=0.08,subsample=0.8,colsample_bytree=0.8,eval_metric="logloss",random_state=42)
xgb.fit(X_train, y_train)
# 4. Predictions
test_pred =xgb.predict(X_test)
train_pred =xgb.predict(X_train)
y_prob = xgb.predict_proba(X_test)[:, 1]
# 5. Evaluation Metrics
print("\nXGBOOST RESULTS")
print("----------------------")

print("Train Accuracy :", accuracy_score(y_train, train_pred))
print(" Test Accuracy :", accuracy_score(y_test, test_pred))
print("Precision:", precision_score(y_test, test_pred))
print("Recall   :", recall_score(y_test, test_pred))
print("F1 Score :", f1_score(y_test, test_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, test_pred))

# -------------------------------------------------
# 6. ROC Curve Plot
# -------------------------------------------------
fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label="XGBoost")
plt.plot([0,1],[0,1],'--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - XGBoost")
plt.legend()
plt.grid()
plt.show()

# -------------------------------------------------
# 7. Feature Importance Plot
# -------------------------------------------------
importances = xgb.feature_importances_
indices = np.argsort(importances)[-10:]

plt.figure(figsize=(8,6))
plt.barh(range(len(indices)), importances[indices])
plt.yticks(range(len(indices)), X.columns[indices])
plt.title("Top 10 Important Features")
plt.show()

# -------------------------------------------------
# 8. Save Model
# -------------------------------------------------
joblib.dump(xgb, "backend/ml/xgboost_model.pkl")
print("\nModel saved successfully.")