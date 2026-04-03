import pandas as pd
import joblib

model = joblib.load("backend/ml/egrantz_model.pkl")


def predict_egrantz(student_dict):

    df = pd.DataFrame([student_dict])

    # Same feature engineering
    df["academic_percentile"] = df["previous_education_percentage"] / 100
    df["financial_need_index"] = 1 / (df["annual_income"] + 1)
    df["scholarship_history_score"] = df["other_scholarship"] * -1.5
    df["merit_need_score"] = (
        df["previous_education_percentage"] * df["financial_need_index"]
    )

    df["top_student_flag"] = (df["previous_education_percentage"] >= 85).astype(int)
    df["low_income_flag"] = (df["annual_income"] <= 200000).astype(int)

    df = pd.get_dummies(df)

    train_cols = model.get_booster().feature_names
    df = df.reindex(columns=train_cols, fill_value=0)

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    if student_dict.get("other_scholarship", 0) == 1:
        probability = probability * 0.1  # reduce probability by 70%
        prediction = 0 if probability < 0.5 else 1

    return prediction, probability