import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score,roc_curve
from imblearn.over_sampling import SMOTE

# -----------------------------
# 1. Load processed dataset
# -----------------------------
data = pd.read_csv("backend/data/clean_ml_dataset.csv")

# -----------------------------
# 2. Separate features & target
# -----------------------------
X = data.drop(columns=["eligible", "egrantz_eligible"])
y = data["egrantz_eligible"]
# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# 3. Apply SMOTE balancing
smote = SMOTE(random_state=42)
X_train_res, y_train_res= smote.fit_resample(X_train, y_train)

print("After SMOTE:", pd.Series(y_train_res).value_counts())
# 5. Train XGBoost model
model = XGBClassifier(n_estimators=250,max_depth=4,learning_rate=0.08,random_state=42,colsample_bytree=0.8,eval_metric="logloss")
model.fit(X_train, y_train)
# 6. Evaluate model
train_pred = model.predict(X_train_res)
test_pred = model.predict(X_test)
print("\nTrain Accuracy:", accuracy_score(y_train_res, train_pred))
print("\nTest Accuracy:", accuracy_score(y_test, test_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, test_pred))

fpr, tpr, _ = roc_curve(y_test, test_pred)

plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label="Egrantz Model")
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
importances = model.feature_importances_
indices = np.argsort(importances)[-10:]

plt.figure(figsize=(8,6))
plt.barh(range(len(indices)), importances[indices])
plt.yticks(range(len(indices)), X.columns[indices])
plt.title("Top 10 Important Features")
plt.show()


# -----------------------------
# 7. Save model
# -----------------------------
joblib.dump(model, "backend/ml/egrantz_model.pkl")

print("\nE-Grantz model saved successfully.")