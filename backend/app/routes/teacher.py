from flask import Blueprint, request, jsonify

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

from database.models import Teacher

# Service
from backend.app.services.user_service import svc_register_teacher, svc_update_teacher
from backend.app.services.teacher_service import (
    svc_teacher_courses,
    svc_teacher_students,
    svc_bulk_attendance,
)

# Schemas
from backend.app.schemas.user_schema import (
    TeacherCreate,
    TeacherRegistrationResponse,
    TeacherProfileRequest,
    TeacherProfile,
)

from backend.app.schemas.teacher_schema import BulkAttendanceUpdate

# Exceptions
from backend.app.exceptions.auth import (
    EmailAlreadyRegisteredError,
    ForbiddenError,
    NotFoundError,
    DuplicateError,
    ValidationError as AppValidationError,
)

# Utils
from backend.app.utils.auth import (
    login_required,
    role_required,
    authorize_teacher_access,
    get_current_user,
)

teacher_bp = Blueprint("teacher", __name__, url_prefix="/api/v1")


@teacher_bp.route("/teachers", methods=["GET"])
def all_teachers():
    teachers = Teacher.query.all()

    response = [TeacherProfile.model_validate(teacher) for teacher in teachers]

    return jsonify([teacher.model_dump(mode="json") for teacher in response]), 200


# Register teacher (Admin/SuperAdmin AUTH route)
@teacher_bp.route("/auth/staff/register", methods=["POST"])
@login_required
@role_required("ADMIN")
def register_teacher():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        teacher_data = TeacherCreate.model_validate(response)

    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "request"
            details[field] = error["msg"].replace("Value error, ", "")

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
        user, teacher = svc_register_teacher(teacher_data)
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
                    "message": "Teacher registration failed.",
                }
            ),
            500,
        )

    teacher_response = TeacherRegistrationResponse(user=user, teacher=teacher)
    return jsonify(teacher_response.model_dump(mode="json")), 201


# Update Teacher Profile (AUTH teacher/admin route)
@teacher_bp.route("/teacher/<string:teacher_id_bus>", methods=["PATCH"])
@login_required
@role_required("TEACHER", "ADMIN")
def update_teacher(teacher_id_bus):

    teacher = Teacher.query.filter_by(teacher_id_bus=teacher_id_bus).first()
    if teacher is None:
        return (
            jsonify(
                {
                    "error": "Not found.",
                    "message": "Teacher not found.",
                }
            ),
            404,
        )

    try:
        authorize_teacher_access(teacher)

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

    response = request.get_json(silent=True)

    # check if request body is supplied
    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        patch_request = TeacherProfileRequest.model_validate(response)

    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "course"
            if error["type"] == "string_pattern_mismatch":
                details[field] = (
                    "Mobile number must be 8 digits long and start with 8 or 9."
                )
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
    update_data = patch_request.model_dump(exclude_unset=True)

    teacher = svc_update_teacher(teacher_id_bus, update_data)

    return (
        jsonify(
            {
                "teacher_id_bus": teacher.teacher_id_bus,
                "salutation": teacher.salutation,
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
                "mobile": teacher.mobile,
                "status": teacher.status,
            }
        ),
        200,
    )


# Password reset


# Assigned Courses
@teacher_bp.route("/teacher/courses", methods=["GET"])
@login_required
@role_required("TEACHER")
def get_teacher_courses():
    try:
        current_user = get_current_user()
        teacher_courses = svc_teacher_courses(user_id=current_user.user_id)
    except NotFoundError as e:
        return (
            jsonify(
                {
                    "error": "Forbidden.",
                    "message": str(e),
                }
            ),
            403,
        )

    return jsonify([course.model_dump(mode="json") for course in teacher_courses]), 200


# View students in each assigned courses
@teacher_bp.route("/teacher/<string:course_id_bus>/students", methods=["GET"])
@login_required
@role_required("TEACHER")
def course_students(course_id_bus):
    try:
        current_user = get_current_user()
        all_students = svc_teacher_students(
            user_id=current_user.user_id, course_id_bus=course_id_bus
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
        jsonify([student.model_dump(mode="json") for student in all_students]),
        200,
    )


# Submit attendance of each student in course (BULK)
@teacher_bp.route("/teacher/<string:course_id_bus>/attendance", methods=["POST"])
@login_required
@role_required("TEACHER")
def students_attendance(course_id_bus):
    try:

        response = request.get_json(silent=True)
        current_user = get_current_user()
        attendance_data = BulkAttendanceUpdate.model_validate(response)
        result = svc_bulk_attendance(
            user_id=current_user.user_id,
            course_id_bus=course_id_bus,
            data=attendance_data,
        )
    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "request"
            details[field] = error["msg"].replace("Value error, ", "")

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

    return jsonify(result), 200
