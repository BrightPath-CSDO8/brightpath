from flask import Blueprint, request, jsonify, session

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

# Schemas
from backend.app.schemas.user_schema import (
    LoginStudentResponse,
    LoginTeacherResponse,
    LoginAdminResponse,
)
from backend.app.schemas.auth_schema import LoginRequest

# Service
from backend.app.services.auth_service import svc_login, svc_me

# Exceptions
from backend.app.exceptions.auth import AuthenticationError

# Utils
from backend.app.utils.auth import login_required, role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1")


@auth_bp.route("/test-student", methods=["GET"])
@login_required
@role_required("STUDENT")
def test_student():
    return jsonify({"message": "Student access granted"}), 200


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

    try:
        user, user_profile = svc_me(user_id)

    except AuthenticationError as e:
        session.clear()

        return (
            jsonify(
                {
                    "error": "Unauthorized.",
                    "message": str(e),
                }
            ),
            401,
        )

    if user.role == "STUDENT":
        response = LoginStudentResponse(
            user=user,
            student=user_profile,
        )

    elif user.role == "TEACHER":
        response = LoginTeacherResponse(
            user=user,
            teacher=user_profile,
        )

    elif user.role == "ADMIN":
        response = LoginAdminResponse(
            user=user,
            admin=user_profile,
        )

    # elif user.role == "SUPERADMIN":
    #     response = LoginSuperAdminResponse(
    #         user=user,
    #         superadmin=user_profile,
    #     )

    else:
        session.clear()

        return (
            jsonify(
                {
                    "error": "Unauthorized.",
                    "message": "Invalid user role.",
                }
            ),
            401,
        )

    return jsonify(response.model_dump(mode="json")), 200


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
        user, user_profile = svc_login(login_user)

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

    if user.role == "STUDENT":
        login_response = LoginStudentResponse(user=user, student=user_profile)
    if user.role == "TEACHER":
        login_response = LoginTeacherResponse(user=user, teacher=user_profile)
    if user.role == "ADMIN":
        login_response = LoginAdminResponse(user=user, admin=user_profile)

    return jsonify(login_response.model_dump(mode="json")), 200


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({"message": "Logout successfully"}), 200
