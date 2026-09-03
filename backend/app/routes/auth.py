from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from app.models.users import User
from app.extensions import db
from pydantic import ValidationError

# Schemas
from app.schemas.user_schema import StudentCreate, StudentResponse, StaffCreate

# Service
from app.services.user_service import svc_register_student, svc_register_staff

# Exceptions
from app.exceptions.auth import EmailAlreadyRegisteredError

auth_bp = Blueprint("auth", __name__)


# Register student
@auth_bp.route("/api/v1/auth/register", methods=["POST"])
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
        print("============================")
        print("ERROR:", e)
        print("ERRORS: ", e.errors())
        print("JSON: ", e.json())
        print("============================")

        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "course"
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
        student = svc_register_student(student_data)
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

    student_response = StudentResponse(
        student_id_bus=student.student_id_bus,
        first_name=student.first_name,
        last_name=student.last_name,
        mobile=student.mobile,
        dob=student.dob,
        role=student.user.role,
    )

    return jsonify(student_response.model_dump(mode="json")), 201


# Login student


# Register for SuperAdmins, Admins, Teachers
# SuperAd -> SuperAd, Admin, Teacher
# Admin -> Teacher
# Hence, to include Bearer Token
@auth_bp.route("/api/v1/auth/staff", methods=["POST"])
def register_staff():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        user_data = StaffCreate.model_validate(response)

    except ValidationError as e:
        pass

    staff = svc_register_staff(user_data)
    # print(f"User: {staff}")

    return (jsonify({"message": "auth user created"}), 201)
