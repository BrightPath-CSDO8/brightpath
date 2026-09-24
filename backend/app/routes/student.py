from flask import Blueprint, request, g, jsonify, session

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

from database.models import Student

# Schemas
from backend.app.schemas.user_schema import (
    StudentCreate,
    StudentRegistrationResponse,
    StudentProfileRequest,
    LoginStudentResponse,
    StudentProfile,
)

# Service
from backend.app.services.user_service import (
    svc_register_student,
    svc_update_student_profile,
)
from backend.app.services.student_service import svc_student_attendance

# Exceptions
from backend.app.exceptions.auth import (
    EmailAlreadyRegisteredError,
    AuthenticationError,
    ForbiddenError,
)

# Utils
from backend.app.utils.auth import (
    login_required,
    role_required,
    authorize_student_access,
    get_current_user,
)

student_bp = Blueprint("student", __name__, url_prefix="/api/v1")


@student_bp.route("/students", methods=["GET"])
def all_students():
    students = Student.query.all()
    response = [StudentProfile.model_validate(student) for student in students]

    return jsonify([student.model_dump(mode="json") for student in response]), 200


# Register student (a public route)
@student_bp.route("/auth/register", methods=["POST"])
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


@student_bp.route("/student/<string:student_id_bus>", methods=["GET"])
@login_required
@role_required("STUDENT", "ADMIN")
def get_one_student(student_id_bus):
    student = Student.query.filter_by(student_id_bus=student_id_bus).first()
    if student is None:
        return (
            jsonify(
                {
                    "error": "Not found.",
                    "message": "Student not found.",
                }
            ),
            404,
        )

    try:
        authorize_student_access(student)

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
    student_profile = StudentProfile.model_validate(student)
    return jsonify(student_profile.model_dump(mode="json")), 200


## UPDATE STUDENT PROFLE
@student_bp.route("/student/<string:student_id_bus>", methods=["PATCH"])
@login_required
@role_required("STUDENT")
def update_student(student_id_bus):
    # Find target student
    student = Student.query.filter_by(student_id_bus=student_id_bus).first()
    if student is None:
        return (
            jsonify(
                {
                    "error": "Not found.",
                    "message": "Student not found.",
                }
            ),
            404,
        )

    try:
        authorize_student_access(student)

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
        patch_request = StudentProfileRequest.model_validate(response)

    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "request"
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

    student = svc_update_student_profile(student_id_bus, update_data)

    return (
        jsonify(
            {
                "student_id_bus": student.student_id_bus,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "mobile": student.mobile,
                "dob": student.dob.isoformat(),
            }
        ),
        200,
    )


# GET STUDENTS' OWN ATTENDANCE
@student_bp.route("/student/attendance", methods=["GET"])
@login_required
@role_required("STUDENT")
def my_attendance():
    current_user = get_current_user()

    result = svc_student_attendance(user_id=current_user.user_id)

    return jsonify(result), 200
