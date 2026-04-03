
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import shap

from sklearn.metrics import confusion_matrix, roc_curve, auc

# -------------------------------------------------
# CREATE PLOT DIRECTORY
# -------------------------------------------------
PLOT_DIR = "backend/visualization/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
raw = pd.read_csv("backend/data/scholarship_dataset_.csv")
clean = pd.read_csv("backend/data/clean_ml_dataset.csv")


# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------
merit_model = joblib.load("backend/ml/xgboost_model.pkl")
egrantz_model = joblib.load("backend/ml/egrantz_model.pkl")

# =================================================
# CLASS IMBALANCE WITH STATISTICS
# =================================================

def plot_class_distribution(df, title, save_name):

    counts = df["eligible"].value_counts()
    total = len(df)

    # Calculate percentages
    pct_0 = counts[0] / total * 100
    pct_1 = counts[1] / total * 100

    # Imbalance ratio
    ratio = counts.max() / counts.min()

    plt.figure(figsize=(6,5))
    sns.barplot(x=counts.index, y=counts.values)

    # Add labels on bars
    for i, v in enumerate(counts.values):
        plt.text(i, v + 10, f"{v}\n({v/total*100:.1f}%)",
                 ha='center', fontsize=10, fontweight='bold')

    plt.title(
        f"{title}\n"
        f"Class 0: {counts[0]} ({pct_0:.1f}%) | "
        f"Class 1: {counts[1]} ({pct_1:.1f}%)\n"
        f"Imbalance Ratio = {ratio:.2f} : 1"
    )

    plt.xlabel("Eligible Class")
    plt.ylabel("Count")

    plt.savefig(f"{PLOT_DIR}/{save_name}.png", dpi=300)
    plt.close()


# Generate BEFORE and AFTER plots
plot_class_distribution(raw, "Before Preprocessing", "class_before")
plot_class_distribution(clean, "After Preprocessing", "class_after")

# =================================================
#  MISSING VALUES COMPARISON
# =================================================
missing_raw = raw.isnull().sum().sum()
missing_clean = clean.isnull().sum().sum()

plt.figure(figsize=(6,5))
bars = plt.bar(["Before Preprocessing","After Preprocessing"],[missing_raw,missing_clean])
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,height,str(int(height)),ha='center',va='bottom')

plt.title("Null Values Comparison")
plt.ylabel("Total Null Count")
plt.savefig("backend/visualization/plots/null_values_comparison.png",dpi=300)
plt.close()

# =================================================
#  CORRELATION HEATMAPS
# =================================================
plt.figure(figsize=(14,6))

plt.subplot(1,2,1)
sns.heatmap(raw.select_dtypes("number").corr(), cmap="coolwarm")
plt.title("Before Preprocessing")

plt.subplot(1,2,2)
sns.heatmap(clean.corr(), cmap="coolwarm")
plt.title("After Preprocessing")

plt.savefig(f"{PLOT_DIR}/correlation_heatmap.png")
plt.close()

# =================================================
# PREPARE DATA FOR MODELS
# =================================================
X_merit = clean.drop(columns=["eligible"])
y_merit = clean["eligible"]

X_merit = X_merit.reindex(
    columns=merit_model.get_booster().feature_names,
    fill_value=0
)

# EGrantz target
y_egrantz = clean["egrantz_eligible"]
X_egrantz = clean.drop(columns=["eligible"])
X_egrantz = X_egrantz.reindex(
    columns=egrantz_model.get_booster().feature_names,
    fill_value=0
)

# =================================================
# FUNCTION TO GENERATE MODEL PLOTS
# =================================================
def generate_model_plots(model, X, y, name):

    # Predictions
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:,1]

    # -----------------------------
    # Confusion Matrix
    # -----------------------------
    cm = confusion_matrix(y, y_pred)
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title(f"Confusion Matrix — {name}")
    plt.savefig(f"{PLOT_DIR}/confusion_{name}.png")
    plt.close()

    # -----------------------------
    # ROC Curve
    # -----------------------------
    fpr, tpr, _ = roc_curve(y, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, label=f"AUC={roc_auc:.3f}")
    plt.plot([0,1],[0,1],'--')
    plt.legend()
    plt.title(f"ROC Curve — {name}")
    plt.savefig(f"{PLOT_DIR}/roc_{name}.png")
    plt.close()

    # -----------------------------
    # Feature Importance
    # -----------------------------
    importance = model.feature_importances_
    indices = np.argsort(importance)[-10:]

    plt.barh(range(len(indices)), importance[indices])
    plt.yticks(range(len(indices)), X.columns[indices])
    plt.title(f"Feature Importance — {name}")
    plt.savefig(f"{PLOT_DIR}/importance_{name}.png")
    plt.close()

    # -----------------------------
    # SHAP PLOTS
    # -----------------------------
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    shap.summary_plot(shap_values, X, show=False)
    plt.savefig(f"{PLOT_DIR}/shap_summary_{name}.png")
    plt.close()

    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.savefig(f"{PLOT_DIR}/shap_bar_{name}.png")
    plt.close()

# =================================================
# GENERATE FOR BOTH MODELS
# =================================================
generate_model_plots(merit_model, X_merit, y_merit, "Merit_Model")
generate_model_plots(egrantz_model, X_egrantz, y_egrantz, "EGrantz_Model")

print("\n ALL VISUALIZATIONS GENERATED SUCCESSFULLY")