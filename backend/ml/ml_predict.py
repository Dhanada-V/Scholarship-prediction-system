import pandas as pd
import joblib

# Load MERIT model
merit_model = joblib.load("backend/ml/xgboost_model.pkl")


def predict_merit(student_dict):
    """
    Predict eligibility using MERIT scholarship model
    """
    df = pd.DataFrame([student_dict])

    # -----------------------------
    # SAME FEATURE ENGINEERING AS TRAINING
    # -----------------------------
    df["academic_percentile"] = df["previous_education_percentage"] / 100
    df["financial_need_index"] = 1 / (df["annual_income"] + 1)
    df["scholarship_history_score"] = df["other_scholarship"] * 1.5

    df["merit_need_score"] = (
        df["previous_education_percentage"] *
        df["financial_need_index"]
    )

    df["top_student_flag"] = (
        df["previous_education_percentage"] >= 85
    ).astype(int)

    df["low_income_flag"] = (
        df["annual_income"] <= 200000
    ).astype(int)

    # -----------------------------
    # ENCODING
    # -----------------------------
    df = pd.get_dummies(df)

    # Align with training columns
    train_cols = merit_model.get_booster().feature_names
    df = df.reindex(columns=train_cols, fill_value=0)

    # -----------------------------
    # Predict
    # -----------------------------
    prediction = int(merit_model.predict(df)[0])
    probability = float(merit_model.predict_proba(df)[0][1])

    return prediction, probability