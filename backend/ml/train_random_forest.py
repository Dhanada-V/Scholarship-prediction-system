import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)

# -------------------------------------------------
# 1. Load engineered dataset
# -------------------------------------------------
DATA_PATH = "backend/data/clean_ml_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

X = df.drop(columns=["eligible","egrantz_eligible"])
y = df["eligible"]

# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)
# 3. Train Random Forest
rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=None,
    min_samples_split=3,
    min_samples_leaf=1,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
# 4. Predictions
train_pred = rf.predict(X_train)
test_prob =rf.predict_proba(X_test)[:,1]
test_pred=(test_prob>=0.4).astype(int)
# 5. Evaluation Metrics
print("\nRANDOM FOREST RESULTS")
print("----------------------")

print("Train Accuracy :", accuracy_score(y_train, train_pred))
print("Test Accuracy :", accuracy_score(y_test, test_pred))
print("Precision:", precision_score(y_test, test_pred))
print("Recall   :", recall_score(y_test, test_pred))
print("F1 Score :", f1_score(y_test, test_pred))
print("ROC-AUC  :", roc_auc_score(y_test, test_prob))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, test_pred))

# -------------------------------------------------
# 6. ROC Curve Plot
# -------------------------------------------------
fpr, tpr, _ = roc_curve(y_test, test_prob)

plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label="Random Forest")
plt.plot([0,1],[0,1],'--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.grid()
plt.show()

# -------------------------------------------------
# 7. Feature Importance Plot
# -------------------------------------------------
importances = rf.feature_importances_
indices = np.argsort(importances)[-10:]

plt.figure(figsize=(8,6))
plt.barh(range(len(indices)), importances[indices])
plt.yticks(range(len(indices)), X.columns[indices])
plt.title("Top 10 Important Features")
plt.show()

# -------------------------------------------------
# 8. Save Model
# -------------------------------------------------
joblib.dump(rf, "backend/ml/random_forest_model.pkl")
print("\nModel saved successfully.")