import os
import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path
from backend.ocr.document_classifier import detect_document_type


def preprocess_image(img):
    """Improve OCR accuracy"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def ocr_with_confidence(img, config):
    data = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DICT)
    text = []
    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 60:
            text.append(data["text"][i])
    return " ".join(text)


def extract_text(file_path):
    if not os.path.exists(file_path):
        return ""

    full_text = ""

    try:
        # ---------- PDF ----------
        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path, dpi=150)

            for img in images:
                img = np.array(img)
                processed = preprocess_image(img)

                raw = pytesseract.image_to_string(processed, config="--psm 3 -l eng")  # was "aw ="
                doc_type = detect_document_type(raw)

                if doc_type == "ACADEMIC":
                    config = "--psm 4 -l eng"
                elif doc_type in ["INCOME", "CASTE"]:
                    config = "--psm 6 -l eng"
                else:
                    full_text += raw  # reuse raw, skip second OCR
                    continue

                full_text += ocr_with_confidence(processed, config)  # was outside the if/else

            return full_text.strip()

        # ---------- IMAGE ----------
        img = cv2.imread(file_path)
        if img is None:
            return ""

        processed = preprocess_image(img)
        raw = pytesseract.image_to_string(processed, config="--psm 3 -l eng")  # removed duplicate assignment
        doc_type = detect_document_type(raw)

        if doc_type == "ACADEMIC":
            config = "--psm 4 -l eng"
        elif doc_type in ["INCOME", "CASTE"]:
            config = "--psm 6 -l eng"
        else:
            return raw.strip()

        return ocr_with_confidence(processed, config).strip()

    except Exception as e:
        print("OCR ERROR:", e)
        return ""