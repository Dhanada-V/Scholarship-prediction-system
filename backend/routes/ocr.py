import os
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage

# OCR modules
from backend.ocr.ocr_engine import extract_text
from backend.ocr.document_classifier import detect_document_type
from backend.ocr.extract_fields import (
    extract_academic_percentage,
    extract_income,
)

# Student profile management
from backend.core.student_profile import (
    reset_student_profile,
    update_student_profile
)




ocr_ns = Namespace(
    "ocr",
    description="Multi-document OCR"
)

# Swagger file upload parser
upload_parser = ocr_ns.parser()
upload_parser.add_argument(
    "files",
    type=FileStorage,
    location="files",
    required=True,
    action="append",
    help="Upload one or more certificates"
)


@ocr_ns.route("/upload-documents")
class MultiOCRUpload(Resource):

    @ocr_ns.expect(upload_parser)
    def post(self):
        """
        Upload documents → Extract data → Build student profile →
        Predict eligibility using ML → Explain using SHAP
        """

        files = request.files.getlist("files")

        if not files:
            return {"error": "No files uploaded"}, 400

        reset_student_profile()
        document_results = []

        for file in files:
            filename = file.filename
            temp_path = f"temp_{filename}"
            file.save(temp_path)

            try:
                text = extract_text(temp_path)
                doc_type = detect_document_type(text)

                extracted = {}

                # -------------------------
                # Academic Certificate
                # -------------------------
                if doc_type == "ACADEMIC":
                    extracted["previous_education_percentage"] = (
                        extract_academic_percentage(text)
                    )

                # -------------------------
                # Income Certificate
                # -------------------------
                if doc_type == "INCOME":
                    extracted["annual_income"] = extract_income(text)

                # Default values
                extracted.setdefault("other_scholarship", 0)

                update_student_profile(extracted)

                document_results.append({
                    "filename": filename,
                    "document_type": doc_type,
                    "status": "processed",
                    "extracted_fields": extracted
                })

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        # -------------------------
        # Final Student Profile
        # -------------------------
        final_profile = update_student_profile({})

        return {
            "documents" : document_results,
            "extracted_student_profile":final_profile
        }, 200