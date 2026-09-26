from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from database.models import Course

# Schemas
from backend.app.schemas.course_schema import (
    CoursePatchRequest,
    CourseCreate,
    CourseResponse,
    CourseStatusEnum,
)

# Service
from backend.app.services.course_service import (
    svc_update_course,
    svc_create_course,
    svc_get_public_courses,
    svc_get_admin_courses,
    svc_get_one_course,
)

# Utils
from backend.app.utils.auth import login_required, role_required

from backend.app.exceptions.auth import (
    NotFoundError,
    ValidationError as AppValidationError,
)

course_bp = Blueprint("course", __name__, url_prefix="/api/v1")


# GET AVAILABLE/OPEN COURSES
@course_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = svc_get_public_courses()

    return jsonify([course.model_dump(mode="json") for course in courses]), 200


# GET ALL COURSES - for ADMINS only
@course_bp.route("/auth/courses", methods=["GET"])
@login_required
@role_required("ADMIN")
def admin_get_courses():
    courses = svc_get_admin_courses()

    return jsonify([course.model_dump(mode="json") for course in courses]), 200


# GET INDIV COURSE
@course_bp.route("/courses/<string:course_id_bus>", methods=["GET"])
def get_one_course(course_id_bus):
    try:
        course = svc_get_one_course(course_id_bus)

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

    return jsonify(course.model_dump(mode="json")), 200


# CREATE COURSE
@course_bp.route("/courses", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_course():
    response = request.get_json(silent=True)

    # check if request body is supplied
    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    # Validate request using Pydantic
    try:
        create_course_req = CourseCreate.model_validate(response)

    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "course"
            if error["type"] == "date_parsing":
                details[field] = "Please provide a valid date."
            else:
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
        course = svc_create_course(create_course_req)
    except NotFoundError as e:
        print(f"e: {e}")
        return (
            jsonify(
                {
                    "error": "Not Found.",
                    "message": str(e),
                }
            ),
            404,
        )
    except AppValidationError as e:
        return (
            jsonify(
                {
                    "error": "Validation Error.",
                    "message": str(e),
                }
            ),
            403,
        )

    return jsonify(course.model_dump(mode="json")), 201


# UPDATE A COURSE
@course_bp.route("/courses/<string:course_id_bus>", methods=["PATCH"])
@login_required
@role_required("ADMIN")
def update_course(course_id_bus):
    response = request.get_json(silent=True)

    # Check if request body is supplied
    if not response:
        return (
            jsonify(
                {
                    "error": "Bad request.",
                    "message": "Request body is required",
                }
            ),
            400,
        )

    # Validate request using Pydantic
    try:
        patch_request = CoursePatchRequest.model_validate(response)

    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "course"

            if error["type"] == "value_error":
                details[field] = str(error["ctx"]["error"])
            else:
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

    # Only include fields that were actually supplied
    update_data = patch_request.model_dump(exclude_unset=True)

    try:
        course = svc_update_course(course_id_bus, update_data)

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

    except ValueError as e:
        return (
            jsonify(
                {
                    "error": "Bad request.",
                    "message": str(e),
                }
            ),
            400,
        )

    # Course itself doesn't exist
    if course is None:
        return (
            jsonify(
                {
                    "error": "Course not found.",
                    "message": "There is no such course",
                }
            ),
            404,
        )

    return (
        jsonify(
            {
                "course_id_bus": course.course_id_bus,
                "course_name": course.course_name,
                "course_fee": float(course.course_fee),
                "description": course.description,
                "schedule": course.schedule,
                "classroom_id": course.classroom_id,
                "teacher_id_us": course.teacher.teacher_id_bus,
                "start_date": (
                    course.start_date.isoformat() if course.start_date else None
                ),
                "end_date": (course.end_date.isoformat() if course.end_date else None),
                "status": course.status,
                "capacity": course.capacity,
            }
        ),
        200,
    )
