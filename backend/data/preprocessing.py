import pandas as pd
import numpy as np

# -----------------------------
# 1. Load RAW dataset
# -----------------------------
INPUT_PATH = "backend/data/scholarship_dataset_.csv"
OUTPUT_PATH = "backend/data/clean_ml_dataset.csv"

df = pd.read_csv(INPUT_PATH)

print("Initial shape:", df.shape)

# -----------------------------
# 2. Remove rule-based / leakage columns
# -----------------------------
rule_based_cols = [
    "student_id",
    "scholarship_id",
    "scholarship_name",
    "min_percentage",
    "max_income",
    "allowed_caste"
]

df = df.drop(columns=[c for c in rule_based_cols if c in df.columns])

print("After removing rule-based columns:", df.shape)

# -----------------------------
# 3. Remove ONLY truly irrelevant sensitive columns
# -----------------------------
# Keep caste_category for E-Grantz ML model

if "religion" in df.columns:
    df = df.drop(columns=["religion"])

if "minority_status" in df.columns:
    df = df.drop(columns=["minority_status"])

print("After removing non-required sensitive attributes:", df.shape)

# -----------------------------
# 4. Handle missing values
# -----------------------------
# Numerical → median
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Categorical → mode
cat_cols = df.select_dtypes(include=["object"]).columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -----------------------------
# 5. Re-generate MERIT eligibility
# -----------------------------
if "eligible" in df.columns:
    df = df.drop(columns=["eligible"])

score = (
    0.5 * (df["previous_education_percentage"] / 100) -
    0.000002 * df["annual_income"] -
    1.0 * df["other_scholarship"]
)

prob = 1 / (1 + np.exp(-score))
#random_values = np.random.rand(len(df))
#df["eligible"] = (random_values<prob).astype(int)
#df["eligible"] = (prob>=prob.median()).astype(int)
noise = np.random.normal(0,0.05,len(df))
#prob = prob+noise
prob = np.clip(prob+noise,0,1)
df["eligible"] =(prob >= 0.5).astype(int)
print("\nMerit Eligibility distribution:")
print(df["eligible"].value_counts(normalize=True))

# -----------------------------
# 6. FEATURE ENGINEERING
# -----------------------------

# Academic percentile
df["academic_percentile"] = df["previous_education_percentage"] / 100

# Financial need index
df["financial_need_index"] = 1 / (df["annual_income"] + 1)

# Scholarship history strength
df["scholarship_history_score"] = df["other_scholarship"] * 1.5

# Merit - Need interaction
#df["merit_need_score"] = (df["previous_education_percentage"] *df["financial_need_index"])

# High performer flag
df["top_student_flag"] = (
    df["previous_education_percentage"] >= 85
).astype(int)

# Low income flag
df["low_income_flag"] = (
    df["annual_income"] <= 200000
).astype(int)

# -----------------------------
# 7. Generate REALISTIC E-Grantz ML Target
# -----------------------------

import numpy as np

#  Convert caste to weight
caste_weight = df["caste_category"].map({
    "SC": 1.0,
    "ST": 1.0,
    "OBC": 0.7,
    "General": 0.0
}).fillna(0)

#  Income need score
income_weight = 1 - (df["annual_income"] / 500000)
income_weight = income_weight.clip(0, 1)

#  Combined eligibility score
egrantz_score = (
    0.6 * caste_weight +
    0.4 * income_weight
)

#  Convert to probability using sigmoid
probability = 1 / (1 + np.exp(-5 * (egrantz_score - 0.5)))

#  Add controlled noise
noise = np.random.normal(0, 0.15, len(df))
probability = np.clip(probability + noise, 0, 1)

#  Final ML label
df["egrantz_eligible"] = (probability >= 0.5).astype(int)

print("\nREALISTIC E-Grantz distribution:")
print(df["egrantz_eligible"].value_counts(normalize=True))
# -----------------------------
#  Encode categorical features
# -----------------------------
df = pd.get_dummies(df)
print("\nAfter encoding:", df.shape)

# -----------------------------
#  Save clean ML dataset
# -----------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("\nPreprocessing complete.")
print("Saved to:", OUTPUT_PATH)