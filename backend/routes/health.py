import os
from flask_restx import Namespace, Resource

health_ns = Namespace("health", description="Backend Health Check API")


@health_ns.route("/")
class HealthCheck(Resource):
    def get(self):
        shap_exists = os.path.exists("backend/ml/shap_values.json")
        model_exists = os.path.exists("backend/ml/model.pkl")

        return {
            "status": "OK",
            "backend": "running",
            "ocr": "available",
            "ml_model_loaded": model_exists,
            "shap_data_available": shap_exists
        }