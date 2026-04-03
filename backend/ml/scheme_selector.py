import pandas as pd
import joblib
from backend.ml.rule_engine import recommend_rule_based_schemes
import os
# Load models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
merit_model = joblib.load("backend/ml/xgboost_model.pkl")
egrantz_model = joblib.load("backend/ml/egrantz_model.pkl")


def predict_with_scheme(student_dict):
    """
    Returns:
    - Merit ML prediction
    - E-Grantz ML prediction
    - Rule-based scholarship recommendations
    """

    df = pd.DataFrame([student_dict])

    # ---------------- MERIT FEATURE ENGINEERING ----------------
    df["academic_percentile"] = df["previous_education_percentage"] / 100
    df["financial_need_index"] = 1 / (df["annual_income"] + 1)
    df["scholarship_history_score"] = df["other_scholarship"] * 1.5
    df["merit_need_score"] = (
        df["previous_education_percentage"] * df["financial_need_index"]
    )
    df["top_student_flag"] = (df["previous_education_percentage"] >= 85).astype(int)
    df["low_income_flag"] = (df["annual_income"] <= 200000).astype(int)

    df_encoded = pd.get_dummies(df)

    # ---------------- MERIT PREDICTION ----------------
    merit_cols = merit_model.get_booster().feature_names
    merit_df = df_encoded.reindex(columns=merit_cols, fill_value=0)

    merit_pred = int(merit_model.predict(merit_df)[0])
    merit_prob = float(merit_model.predict_proba(merit_df)[0][1])

    # ---------------- EGRANTZ PREDICTION ----------------
    #egrantz_cols = egrantz_model.get_booster().feature_names
    #egrantz_df = df_encoded.reindex(columns=egrantz_cols, fill_value=0)

    #egrantz_pred = int(egrantz_model.predict(egrantz_df)[0])
    #egrantz_prob = float(egrantz_model.predict_proba(egrantz_df)[0][1])
    from backend.ml.predict_egrantz import predict_egrantz
    egrantz_pred ,egrantz_prob=predict_egrantz(student_dict)

    # ---------------- RULE ENGINE ----------------
    rule_recommendations = recommend_rule_based_schemes(student_dict)

    return {
        "ml_predictions": {
            "merit_scholarship": {
                "eligible": bool(merit_pred),
                "probability": round(merit_prob, 3)
            },
            "egrantz_scholarship": {
                "eligible": bool(egrantz_pred),
                "probability": round(egrantz_prob, 3)
            }
        },
        "rule_based_recommendations": rule_recommendations
    }