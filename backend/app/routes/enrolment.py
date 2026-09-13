from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from database.models import Enrolment

# Schemas
from backend.app.schemas.enrolment_schema import (
    EnrolmentCreate,
    AdminUpdateEnrolment,
)

# Service
from backend.app.services.enrolment_service import (
    svc_create_enrolment,
    svc_student_enrolments,
    svc_admin_enrolments,
    svc_admin_update_enrolment,
)

# Utils
from backend.app.utils.auth import login_required, role_required, get_current_user

# Exceptions
from backend.app.exceptions.auth import NotFoundError, DuplicateError, ForbiddenError

enrol_bp = Blueprint("enrol", __name__, url_prefix="/api/v1")


# ALL ENROLMENTS (for ADMINS only)
# TODO: Search by Stu-ID
# TODO: Search by Course-ID
@enrol_bp.route("/auth/enrolments", methods=["GET"])
def admin_enrolments():
    try:
        status_filter = request.args.get("status")
        enrolment_list = svc_admin_enrolments(status=status_filter)
        return (
            jsonify([enrolment for enrolment in enrolment_list]),
            200,
        )
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@enrol_bp.route("/enrolment", methods=["POST"])
@login_required
@role_required("STUDENT")
def create_enrolment():
    current_user = get_current_user()
    response = request.get_json(silent=True)
    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )
    try:
        create_enrol_req = EnrolmentCreate.model_validate(response)
    except ValidationError as e:
        return jsonify({"error": "Invalid request.", "errors": e.errors()}), 400
    enrolment_req = create_enrol_req.model_dump(exclude_unset=True)
    print(f"route enr: {enrolment_req}")
    try:
        enrolment_response = svc_create_enrolment(
            data=enrolment_req, user_id=current_user.user_id
        )
    except ForbiddenError as e:
        return (
            jsonify(
                {
                    "error": "Forbidden.",
                    "message": str(e),
                }
            ),
            403,
        )
    except NotFoundError as e:
        return (
            jsonify(
                {
                    "error": "Not Found.",
                    "message": str(e),
                }
            ),
            404,
        )
    except DuplicateError as e:
        return (
            jsonify(
                {
                    "error": "Conflict.",
                    "message": str(e),
                }
            ),
            409,
        )

    return jsonify(enrolment_response.model_dump(mode="json")), 201


# ALL ENROLMENTS (for STUDENTS only)
@enrol_bp.route("/enrolments", methods=["GET"])
@login_required
@role_required("STUDENT")
def get_student_enrolments():
    current_user = get_current_user()
    try:
        filter_status = request.args.get("status")
        student_enrolments = svc_student_enrolments(
            user_id=current_user.user_id, status=filter_status
        )
    except ForbiddenError as e:
        return (
            jsonify(
                {
                    "error": "Forbidden.",
                    "message": str(e),
                }
            ),
            403,
        )

    return (
        jsonify(
            [enrolment.model_dump(mode="json") for enrolment in student_enrolments]
        ),
        200,
    )


# UPDATE ENROLMENT BY ADMIN (simplified payment approval)
@enrol_bp.route("/enrolment/<string:enrolment_id_bus>", methods=["PATCH"])
@login_required
@role_required("ADMIN")
def admin_update_student_enrolment(enrolment_id_bus):
    response = request.get_json(silent=True)
    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )
    try:
        patch_request = AdminUpdateEnrolment.model_validate(response)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "error": "Invalid request.",
                    "errors": e.errors(),
                }
            ),
            400,
        )
    try:
        update_enrol_req = svc_admin_update_enrolment(
            enrolment_id_bus=enrolment_id_bus, data=patch_request
        )
    except NotFoundError as e:
        return (
            jsonify(
                {
                    "error": "Not Found.",
                    "message": str(e),
                }
            ),
            404,
        )
    return jsonify({"message": "Enrolment updated successfully"}), 200
