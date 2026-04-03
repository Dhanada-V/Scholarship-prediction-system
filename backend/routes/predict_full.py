from flask_restx import Namespace, Resource, fields
from backend.ml.scheme_selector import predict_with_scheme
from backend.ml.shap_service import explain_student

predict_full_ns = Namespace("predict", description="Final AI Eligibility API")

student_model = predict_full_ns.model("StudentInput", {
    "previous_education_percentage": fields.Float(required=True),
    "annual_income": fields.Float(required=True),
    "other_scholarship": fields.Float(required=True),
    "caste_category": fields.String(required=True),
    "religion": fields.String(required=False),
    "stream": fields.String(required=False),
    "gender": fields.String(required=False),
    "single_child": fields.Boolean(required=False)
})


@predict_full_ns.route("/full")
class PredictFull(Resource):

    @predict_full_ns.expect(student_model)
    def post(self):
        try:
            data = predict_full_ns.payload

            # ---------------- ML + RULE PREDICTION ----------------
            result = predict_with_scheme(data)

            ml_predictions = result["ml_predictions"]
            rule_schemes = result["rule_based_recommendations"]

            # ---------------- SHAP EXPLANATION ----------------
            explanations = explain_student(data)

            # ---------------- HUMAN SUMMARY ----------------
            merit_prob = ml_predictions["merit_scholarship"]["probability"]

            if merit_prob >= 0.7:
                overall = "HIGHLY ELIGIBLE"
            elif merit_prob >= 0.5:
                overall = "LIKELY ELIGIBLE"
            else:
                overall = "LOW ELIGIBILITY"

            summary = {
            "overall_eligibility": overall,
            "key_strength": "Strong academic performance and financial need",
            "recommended_action": "Apply for eligible schemes shown below"
             }

            # ---------------- FINAL RESPONSE ----------------
            return {
            "ml_predictions": ml_predictions,
            "rule_based_schemes": rule_schemes,
            "final_summary": summary,
            "explanations": explanations
            }
        except Exception as e:
            print("Backend Error:",str(e))
            return {
                "error :",str(e)
            },500

