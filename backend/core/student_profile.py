# Temporary in-memory storage
student_profile = {
    "previous_percentage": None,
    "annual_income": None,
    "caste_category": None,
    "religion": None,
}

def reset_student_profile():
    global student_profile
    student_profile = {
        "previous_percentage": None,
        "annual_income": None,
        "caste_category": None,
        "religion": None
    }

def update_student_profile(extracted_data: dict):
    """
    Update student profile only with non-null values
    """
    for key, value in extracted_data.items():
        if value is not None:
            student_profile[key] = value

    return student_profile
