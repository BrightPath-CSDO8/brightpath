from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from database.models import Classroom

# Schema
from backend.app.schemas.classroom_schema import ClassroomCreate, AllClassrooms

# Service
from backend.app.services.classroom_service import svc_create_classroom

# Utils
from backend.app.utils.auth import login_required, role_required

classroom_bp = Blueprint("classroom", __name__)


@classroom_bp.route("/api/v1/classrooms", methods=["GET"])
# @login_required()
# @role_required("ADMIN", "SUPERADMIN")
def get_all_classrooms():
    classrooms = Classroom.query.all()

    response = [AllClassrooms.model_validate(classrooms) for classrooms in classrooms]

    return jsonify([classroom.model_dump(mode="json") for classroom in response]), 200


@classroom_bp.route("/api/v1/classroom", methods=["POST"])
# @login_required()
# @role_required("ADMIN", "SUPERADMIN")
def create_classroom():
    response = request.get_json(silent=True)

    # check if request body is supplied
    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        create_classroom = ClassroomCreate.model_validate(response)
    except ValidationError as e:

        details = {}
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "classes"
            details[field] = error["msg"]

        return (
            jsonify(
                {
                    "error": "Bad request.",
                    "message": "Invalid request body.",
                    "details": details,
                }
            ),
            400,
        )

    classroom = svc_create_classroom(create_classroom)

    return (
        jsonify(
            {
                "id": classroom.id,
                "room_name": classroom.room_name,
                "class_capacity": classroom.class_capacity,
            }
        ),
        201,
    )
