import pandas as pd
import joblib
import shap

model = joblib.load("backend/ml/xgboost_model.pkl")
explainer = shap.TreeExplainer(model)


def explain_student(student_dict):

    df = pd.DataFrame([student_dict])

    # Feature engineering
    df["academic_percentile"] = df["previous_education_percentage"] / 100
    df["financial_need_index"] = 1 / (df["annual_income"] + 1)
    df["scholarship_history_score"] = df["other_scholarship"] * 1.5
    df["merit_need_score"] = (
        df["previous_education_percentage"] * df["financial_need_index"]
    )
    df["top_student_flag"] = (df["previous_education_percentage"] >= 85).astype(int)
    df["low_income_flag"] = (df["annual_income"] <= 200000).astype(int)

    df_encoded = pd.get_dummies(df)

    cols = model.get_booster().feature_names
    df_encoded = df_encoded.reindex(columns=cols, fill_value=0)

    prob = model.predict_proba(df_encoded)[0][1]

    explanations = []

    # ---------- OVERALL RESULT ----------
    if prob >= 0.7:
        explanations.append("You are HIGHLY likely to receive a merit scholarship.")
    elif prob >= 0.4:
        explanations.append("You have MODERATE chances of receiving a scholarship.")
    else:
        explanations.append("Your chances of receiving a merit scholarship are LOW.")

    explanations.append(f"Eligibility confidence: {round(prob*100,1)}%")

    # ---------- ACADEMIC ----------
    marks = student_dict["previous_education_percentage"]

    if marks >= 90:
        explanations.append("Excellent academic performance strongly improved eligibility.")
    elif marks >= 75:
        explanations.append("Good academic performance supported eligibility.")
    elif marks >= 60:
        explanations.append("Average academic performance provided limited support.")
    else:
        explanations.append("Low academic performance significantly reduced eligibility.")

    # ---------- INCOME ----------
    income = student_dict["annual_income"]

    if income <= 200000:
        explanations.append("Low family income positively influenced eligibility.")
    elif income <= 500000:
        explanations.append("Moderate income slightly reduced priority.")
    else:
        explanations.append("Higher income significantly reduced eligibility priority.")

    # ---------- SCHOLARSHIP HISTORY ----------
    other = student_dict["other_scholarship"]

    if other > 0:
        explanations.append("Receiving other scholarships reduced your selection priority.")
    else:
        explanations.append("No previous scholarships improved your selection chances.")

    return explanations