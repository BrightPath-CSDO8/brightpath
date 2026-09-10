from flask import Blueprint, request, jsonify, session

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

from database.models import Users
from database.models import Student

# Schemas
from backend.app.schemas.user_schema import (
    StudentCreate,
    StudentResponse,
    StaffCreate,
    LoginStudentResponse,
    StudentRegistrationResponse,
)
from backend.app.schemas.auth_schema import LoginRequest

# Service
from backend.app.services.user_service import svc_register_student, svc_register_staff
from backend.app.services.auth_service import svc_login

# Exceptions
from backend.app.exceptions.auth import EmailAlreadyRegisteredError, AuthenticationError

# Utils
from backend.app.utils.auth import login_required, role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1")


@auth_bp.route("/test-student", methods=["GET"])
@login_required
@role_required("STUDENT")
def test_student():
    return jsonify({"message": "Student access granted"}), 200


# AUTH ME
# use this endpoint if users refreshes the page
@auth_bp.route("/auth/me", methods=["GET"])
def auth_me():
    user_id = session.get("user_id")
    if not user_id:
        return (
            jsonify(
                {
                    "error": "Unauthorized.",
                    "message": "User is not authenticated.",
                }
            ),
            401,
        )
    user = Users.query.get(user_id)

    if not user:
        session.clear()

        return jsonify(
            {
                "error": "Unauthorized.",
                "message": "User account not found.",
            }
        )

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return (
            jsonify(
                {
                    "error": "Unauthorized.",
                    "message": "Student profile not found.",
                }
            ),
            401,
        )
    response = LoginStudentResponse(
        user=user,
        student=student,
    )
    return jsonify(response.model_dump(mode="json")), 200


# Login
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        login_user = LoginRequest.model_validate(response)
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

    try:
        user, student = svc_login(login_user)

    except AuthenticationError as e:
        return (
            jsonify(
                {
                    "error": "Unauthorized.",
                    "message": str(e),
                }
            ),
            401,
        )

    session["user_id"] = user.user_id
    session["role"] = user.role
    login_response = LoginStudentResponse(user=user, student=student)
    # print(f"User login: {login_response}")

    return jsonify(login_response.model_dump(mode="json")), 200
    # return jsonify({"message": "Login successfully"})


# Logout
@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({"message": "Logout successfully"}), 200


# Register student (a public route)
@auth_bp.route("/auth/register", methods=["POST"])
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


# Register for SuperAdmins, Admins, Teachers
# SuperAd -> SuperAd, Admin, Teacher
# Admin -> Teacher
@auth_bp.route("/auth/staff", methods=["POST"])
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
