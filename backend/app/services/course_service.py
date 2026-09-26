from backend.app.extensions import db

from database.models import Course, Teacher, Classroom
from backend.app.schemas.course_schema import CourseResponse
from backend.app.utils import generate_business_id
from backend.app.exceptions.auth import (
    NotFoundError,
    ValidationError as AppValidationError,
)


def svc_get_admin_courses():
    stmt = db.select(Course).join(Teacher, Course.teacher_id == Teacher.teacher_id)

    courses = db.session.scalars(stmt).all()

    return [
        CourseResponse(
            course_id_bus=course.course_id_bus,
            course_name=course.course_name,
            course_fee=float(course.course_fee),
            description=course.description,
            schedule=course.schedule,
            start_date=course.start_date,
            end_date=course.end_date,
            capacity=course.capacity,
            teacher_id_bus=course.teacher.teacher_id_bus,
            classroom_id=course.classroom_id,
            status=course.status,
        )
        for course in courses
    ]


def svc_get_public_courses():
    stmt = (
        db.select(Course)
        .join(Teacher, Course.teacher_id == Teacher.teacher_id)
        .where(Course.status == "OPEN")
    )

    courses = db.session.scalars(stmt).all()

    return [
        CourseResponse(
            course_id_bus=course.course_id_bus,
            course_name=course.course_name,
            course_fee=float(course.course_fee),
            description=course.description,
            schedule=course.schedule,
            start_date=course.start_date,
            end_date=course.end_date,
            capacity=course.capacity,
            teacher_id_bus=course.teacher.teacher_id_bus,
            classroom_id=course.classroom_id,
            status=course.status,
        )
        for course in courses
    ]


def svc_get_one_course(course_id_bus: str):
    stmt = db.select(Course).where(Course.course_id_bus == course_id_bus)

    course = db.session.scalar(stmt)

    if not course:
        raise NotFoundError("Course not found.")

    return CourseResponse(
        course_id_bus=course.course_id_bus,
        course_name=course.course_name,
        course_fee=float(course.course_fee),
        description=course.description,
        schedule=course.schedule,
        start_date=course.start_date,
        end_date=course.end_date,
        capacity=course.capacity,
        teacher_id_bus=course.teacher.teacher_id_bus,
        classroom_id=course.classroom_id,
        status=course.status,
    )


def svc_create_course(data):
    # Unique ID generation loop using modern 2.0 syntax
    while True:

        # Check if Teacher Id is available && ACTIVE
        stmt_teacher_user = db.select(Teacher).where(
            Teacher.teacher_id_bus == data.teacher_id_bus
        )
        existing_teacher = db.session.scalar(stmt_teacher_user)

        if not existing_teacher:
            raise NotFoundError("Teacher is not found in system.")

        if existing_teacher.status != "ACTIVE":
            raise AppValidationError(
                "Course can only be assigned to an active teacher."
            )

        # Check if Classroom Id is available
        stmt_classroom = db.select(Classroom.classroom_id).where(
            Classroom.classroom_id == data.classroom_id
        )
        existing_classroom_id = db.session.scalar(stmt_classroom)

        if not existing_classroom_id:
            raise NotFoundError("Classroom is not found in system.")

        generated_id = generate_business_id("CSR")

        # db.select() replaces Course.query
        # Builds the DB query:
        stmt = db.select(Course).where(Course.course_id_bus == generated_id)
        # Then send to DB, execute it and return the first scalar result
        existing_course = db.session.scalar(stmt)

        # If no collision is found, break out and use this ID
        if not existing_course:
            course_id_bus = generated_id
            break

    # Instantiate the ORM object using consistent Pydantic dot notation
    course = Course(
        course_id_bus=course_id_bus,
        course_name=data.course_name,
        course_fee=data.course_fee,
        description=data.description,
        schedule=data.schedule,
        start_date=data.start_date,
        end_date=data.end_date,
        capacity=data.capacity,
        status="PENDING",
        teacher_id=existing_teacher.teacher_id,
        classroom_id=existing_classroom_id,
    )

    db.session.add(course)
    db.session.commit()

    return CourseResponse(
        course_id_bus=course.course_id_bus,
        course_name=course.course_name,
        course_fee=float(course.course_fee),
        description=course.description,
        schedule=course.schedule,
        # classroom= course.classroom.room_name if course.classroom else None,
        classroom_id=course.classroom_id,
        teacher_id_bus=existing_teacher.teacher_id_bus,
        start_date=course.start_date,
        end_date=course.end_date,
        status=course.status,
        capacity=course.capacity,
    )


def svc_update_course(course_id_bus, update_data):
    # 1. Find the course
    stmt_course = db.select(Course).where(Course.course_id_bus == course_id_bus)

    course = db.session.scalar(stmt_course)

    if course is None:
        return None

    # 2. Check teacher if teacher_id_bus is being updated
    if "teacher_id_bus" in update_data:
        stmt_teacher = db.select(Teacher).where(
            Teacher.teacher_id_bus == update_data["teacher_id_bus"]
        )

        teacher = db.session.scalar(stmt_teacher)

        if teacher is None:
            raise NotFoundError("Teacher is not found in system.")

        update_data["teacher_id"] = teacher.teacher_id

        del update_data["teacher_id_bus"]

    # 3. Check classroom if classroom_id is being updated
    if "classroom_id" in update_data:
        stmt_classroom = db.select(Classroom).where(
            Classroom.classroom_id == update_data["classroom_id"]
        )

        classroom = db.session.scalar(stmt_classroom)

        if classroom is None:
            raise NotFoundError("Classroom is not found in system.")

    # 4. Check dates against the existing course
    new_start_date = update_data.get("start_date", course.start_date)
    new_end_date = update_data.get("end_date", course.end_date)

    if new_start_date >= new_end_date:
        raise ValueError("End date must be after start date.")

    # 5. Apply the patch only after all validation passes
    for field, value in update_data.items():
        setattr(course, field, value)

    db.session.commit()

    return course
