from flask import Blueprint, request, jsonify

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

from database.models import Admin

# Schemas
from backend.app.schemas.user_schema import (
    AdminProfile,
    AdminCreate,
    AdminCreateResponse,
)

# Service
from backend.app.services.user_service import svc_register_admin

# Exceptions
from backend.app.exceptions.auth import EmailAlreadyRegisteredError, ForbiddenError

# Utils
from backend.app.utils.auth import login_required, role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1")


@admin_bp.route("/admins", methods=["GET"])
def all_admins():
    admins = Admin.query.all()

    response = [AdminProfile.model_validate(admin) for admin in admins]

    return jsonify([admin.model_dump(mode="json") for admin in response]), 200


@admin_bp.route("/auth/admin/register", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_admin():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        admin_data = AdminCreate.model_validate(response)

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
        user, admin = svc_register_admin(admin_data)
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
        return (
            jsonify(
                {
                    "error": "Internal server error.",
                    "message": "Admin registration failed.",
                }
            ),
            500,
        )

    admin_response = AdminCreateResponse(user=user, admin=admin)
    return jsonify(admin_response.model_dump(mode="json")), 201
