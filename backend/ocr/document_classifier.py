def detect_document_type(text: str) -> str:
    if not text:
        return "UNKNOWN"

    t = text.lower()

    #  INCOME CERTIFICATE
    if any(k in t for k in [
        "income certificate",
        "annual family income",
        "form 10c",
        "rupees",
        "₹"
    ]):
        return "INCOME"

    # ACADEMIC DOCUMENT
    if any(k in t for k in [
        "grade",
        "semester",
        "cgpa",
        "marks",
        "university",
        "consolidated"
    ]):
        return "ACADEMIC"

    #  CASTE CERTIFICATE
    if any(k in t for k in [
        "caste certificate",
        "scheduled caste",
        "scheduled tribe",
        "community"
    ]):
        return "CASTE"

    return "UNKNOWN"
