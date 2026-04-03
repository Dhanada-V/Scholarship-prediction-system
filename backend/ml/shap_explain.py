import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

# -------------------------------------------------
# Load dataset and model
# -------------------------------------------------
data = pd.read_csv("backend/data/clean_ml_dataset.csv")
model = joblib.load("backend/ml/xgboost_model.pkl")

X = data.drop(columns=["eligible","egrantz_eligible"])

# -------------------------------------------------
# Create SHAP explainer
# -------------------------------------------------
explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X)

# -------------------------------------------------
#  GLOBAL FEATURE IMPORTANCE
# -------------------------------------------------
shap.summary_plot(shap_values, X)

# -------------------------------------------------
#  FEATURE IMPACT (Bar Plot)
# -------------------------------------------------
shap.summary_plot(shap_values, X, plot_type="bar")

# -------------------------------------------------
#  LOCAL EXPLANATION FOR ONE STUDENT
# -------------------------------------------------
student_index = 5
shap.force_plot(
    explainer.expected_value,
    shap_values[student_index],
    X.iloc[student_index],
    matplotlib=True
)

plt.show()