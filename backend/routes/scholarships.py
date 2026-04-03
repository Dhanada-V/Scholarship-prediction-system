from flask_restx import Namespace, Resource

scholarships_ns = Namespace(
    "scholarships",
    description="Scholarship Information APIs"
)

SCHOLARSHIPS = [
    {
        "id": "PM",
        "name": "Post-Matric Minority Scholarship",
        "description": "For minority students with income ≤ ₹2,00,000"
    },
    {
        "id": "EG",
        "name": "E-Grantz Scholarship",
        "description": "For SC/ST/OBC students (Kerala Govt.)"
    },
    {
        "id": "SM",
        "name": "State Merit Scholarship",
        "description": "For UG students with high academic merit"
    },
    {
        "id": "IN",
        "name": "INSPIRE Scholarship",
        "description": "For UG Science students"
    },
    {
        "id": "SG",
        "name": "Single Girl Child Scholarship",
        "description": "For single girl children"
    }
]

@scholarships_ns.route("/")
class ScholarshipList(Resource):
    def get(self):
        return {
            "count": len(SCHOLARSHIPS),
            "scholarships": SCHOLARSHIPS
        }
