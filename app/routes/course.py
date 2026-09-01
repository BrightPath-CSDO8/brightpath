from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.course import Course
from pydantic import ValidationError

# Schemas
from app.schemas.course_schema import CoursePatchRequest, CourseCreate

# Service
from app.services.course_service import svc_update_course, svc_create_course

course_bp = Blueprint("course", __name__)


# GET ALL COURSES
@course_bp.route("/api/v1/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    return [
        {
            "course_id_bus": course.course_id_bus,
            "course_name": course.course_name,
            "course_fee": float(course.course_fee),
            "description": course.description,
            "schedule": course.schedule,
            "start_date": course.start_date.isoformat() if course.start_date else None,
            "end_date": course.end_date.isoformat() if course.end_date else None,
            "status": course.status,
            "capacity": course.capacity,
        }
        for course in courses
    ]


# CREATE COURSE
@course_bp.route("/api/v1/courses", methods=["POST"])
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
        create_request = CourseCreate.model_validate(response)

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
    course_req = create_request.model_dump(exclude_unset=True)

    course = svc_create_course(course_req)

    # return created course
    return (
        jsonify(
            {
                "course_id_bus": course.course_id_bus,
                "course_name": course.course_name,
                "course_fee": float(course.course_fee),
                "description": course.description,
                "schedule": course.schedule,
                "start_date": (
                    course.start_date.isoformat() if course.start_date else None
                ),
                "end_date": (course.end_date.isoformat() if course.end_date else None),
                "status": course.status,
                "capacity": course.capacity,
            }
        ),
        201,
    )


# UPDATE A COURSE
@course_bp.route("/api/v1/courses/<string:course_id_bus>", methods=["PATCH"])
def update_course(course_id_bus):
    response = request.get_json(silent=True)

    # check if request body is supplied
    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )
    # Validate request using Pydantic
    try:
        patch_request = CoursePatchRequest.model_validate(response)

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
    update_data = patch_request.model_dump(exclude_unset=True)

    course = svc_update_course(course_id_bus, update_data)

    if course is None:
        return (
            jsonify(
                {"error": "Course not found.", "message": "There is no such course"}
            ),
            404,
        )

    # Return updated course
    return (
        jsonify(
            {
                "course_id_bus": course.course_id_bus,
                "course_name": course.course_name,
                "course_fee": float(course.course_fee),
                "description": course.description,
                "schedule": course.schedule,
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
