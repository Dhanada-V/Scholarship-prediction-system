from flask import Flask
from flask_restx import Api
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"]= 100*1024*1024
    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["MAX_FORM_MEMORY_SIZE"] = 100 * 1024 * 1024
    CORS(app)

    api = Api(
        app,
        title="Scholarship Eligibility System",
        version="1.0",
        description="Rule-based + ML Scholarship Eligibility API with Explainability"
    )

    # Import namespaces
    from backend.routes.health import health_ns
    from backend.routes.scholarships import scholarships_ns
    from backend.routes.ocr import ocr_ns
    from backend.routes.predict_full import predict_full_ns

    # Register namespaces
    api.add_namespace(health_ns, path="/health")
    api.add_namespace(scholarships_ns, path="/scholarships")
    api.add_namespace(ocr_ns, path="/ocr")
    api.add_namespace(predict_full_ns, path="/predict_full")

    return app


#  REQUIRED to actually run backend
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)