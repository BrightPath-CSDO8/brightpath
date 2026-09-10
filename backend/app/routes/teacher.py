from flask import Blueprint, request, jsonify, session

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

from database.models import Student

# Schemas
from backend.app.schemas.user_schema import (
    StudentCreate,
    StudentRegistrationResponse,
)

# Service
from backend.app.services.user_service import svc_register_student

# Exceptions
from backend.app.exceptions.auth import EmailAlreadyRegisteredError, AuthenticationError

# Utils
from backend.app.utils.auth import login_required, role_required

teacher_bp = Blueprint("teacher", __name__, url_prefix="/api/v1")


# Register teacher (a Admin/SuperAdmin AUTH route)
@teacher_bp.route("/auth/register", methods=["POST"])
def register_student():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        student_data = StudentCreate.model_validate(response)

    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "request"
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
    # 2. Perform registration operation
    try:
        user, student = svc_register_student(student_data)
    except EmailAlreadyRegisteredError as e:
        return (
            jsonify(
                {
                    "error": "Conflict.",
                    "message": str(e),
                }
            ),
            409,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "error": "Conflict.",
                    "message": "Registration conflicts with existing data.",
                }
            ),
            409,
        )
    except Exception as e:
        print("Registration failed:", e)

        return (
            jsonify(
                {
                    "error": "Internal server error.",
                    "message": "Student registration failed.",
                }
            ),
            500,
        )

    student_response = StudentRegistrationResponse(user=user, student=student)

    return jsonify(student_response.model_dump(mode="json")), 201


# Update Teacher Profile (auth route)
@teacher_bp.route("/teacher", methods=["PATCH"])
def patch_teacher():
    pass
