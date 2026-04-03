import re


def extract_academic_percentage(text):
    patterns = [
        r'percentage\s*[:\-]?\s*(\d{2}\.?\d?)',
        r'(\d{2}\.?\d?)\s*%',
        r'cgpa\s*[:\-]?\s*(\d\.\d{1,2})'
    ]

    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return float(m.group(1))

    return None


import re

def extract_income(text):
    if not text:
        return None

    clean_text = text.replace(",", "").lower()

    #  FIRST PRIORITY: Numeric income (₹ 84000)
    num_match = re.search(r'₹\s*(\d{4,7})', clean_text)
    if num_match:
        return int(num_match.group(1))

    #  Rs. 84000
    num_match = re.search(r'rs\.?\s*(\d{4,7})', clean_text)
    if num_match:
        return int(num_match.group(1))

    # Annual income ... 84000
    num_match = re.search(r'annual\s+family\s+income.*?(\d{4,7})', clean_text)
    if num_match:
        return int(num_match.group(1))

    #  Word-based income
    word_match = re.search(r'rupees\s+([a-z\s]+?)\s+only', clean_text)
    if word_match:
        income_words = word_match.group(1)
        return words_to_number(income_words)

    return None


def extract_caste(text):
    if not text:
        return None

    if re.search(r'\b(sc|scheduled caste)\b', text, re.I):
        return "SC"
    if re.search(r'\b(st|scheduled tribe)\b', text, re.I):
        return "ST"
    if re.search(r'\b(obc|other backward)\b', text, re.I):
        return "OBC"

    return None


def extract_religion(text):
    if re.search(r'muslim', text, re.I):
        return "Muslim"
    if re.search(r'christian', text, re.I):
        return "Christian"
    if re.search(r'hindu', text, re.I):
        return "Hindu"
    return None

def words_to_number(words):
    """
    Convert basic English number words to integer.
    Handles up to lakhs.
    """
    word_map = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20, "thirty": 30, "forty": 40,
        "fifty": 50, "sixty": 60, "seventy": 70,
        "eighty": 80, "ninety": 90
    }

    multipliers = {
        "hundred": 100,
        "thousand": 1000,
        "lakh": 100000,
        "lakhs": 100000
    }

    total = 0
    current = 0

    for word in words.lower().split():
        if word in word_map:
            current += word_map[word]
        elif word in multipliers:
            current *= multipliers[word]
            total += current
            current = 0

    return total + current if total > 0 else None
