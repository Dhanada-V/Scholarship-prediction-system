def recommend_rule_based_schemes(student):

    recommendations = []

    # Normalize inputs
    income = student.get("annual_income", 0)
    marks = student.get("previous_education_percentage", 0)
    religion = student.get("religion", "").lower()
    stream = student.get("stream", "").lower()
    gender = student.get("gender", "").lower()
    single_child = student.get("single_child", False)

    # -----------------------------
    # Post-Matric Minority Scholarship
    # -----------------------------
    minority_religions = ["christian", "muslim", "sikh", "buddhist"]

    if religion in minority_religions and income <= 200000:
        recommendations.append({
            "scheme": "Post-Matric Minority Scholarship",
            "eligible": True,
            "reason": "You belong to a minority religion and your income is below ₹2,00,000"
        })

    # -----------------------------
    # INSPIRE Scholarship (REALISTIC RULE)
    # -----------------------------

    science_fields = [
        "physics", "chemistry", "mathematics", "biology",
        "statistics", "geology", "bsc", "msc"
    ]

    excluded_fields = [
        "engineering", "btech", "medicine", "mbbs",
        "technology", "professional"
    ]

    stream_lower = stream.lower()

    is_science = any(k in stream_lower for k in science_fields)
    is_excluded = any(k in stream_lower for k in excluded_fields)

    if is_science and not is_excluded and marks >= 85:
        recommendations.append({
            "scheme": "INSPIRE Scholarship",
            "eligible": True,
            "reason": "You are pursuing a basic science course and scored above 85%"
        })
    # -----------------------------
    # State Merit Scholarship
    # -----------------------------
    if marks >= 90:
        recommendations.append({
            "scheme": "State Merit Scholarship",
            "eligible": True,
            "reason": "You have excellent academic performance above 90%"
        })

    # -----------------------------
    # Single Girl Child Scholarship
    # -----------------------------
    if gender == "female" and single_child:
        recommendations.append({
            "scheme": "Single Girl Child Scholarship",
            "eligible": True,
            "reason": "You are a female student and the only child"
        })

    return recommendations