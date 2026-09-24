from backend.app.extensions import db

from database.models import (
    Users,
    Teacher,
    Student,
    Course,
    Enrolment,
    Attendance,
    Grade,
)

# Exceptions
from backend.app.exceptions.auth import (
    DuplicateError,
    NotFoundError,
    ForbiddenError,
    ValidationError as AppValidationError,
)


def svc_student_attendance(user_id: int):
    # --------------------------------------------------
    # 1. Resolve current student's internal ID
    # --------------------------------------------------
    student_stmt = (
        db.select(Student.student_id)
        .join(Users, Student.user_id == Users.user_id)
        .where(Users.user_id == user_id)
    )

    student_internal_id = db.session.scalar(student_stmt)

    if not student_internal_id:
        raise ForbiddenError("Current user is not a Student in the system.")

    # --------------------------------------------------
    # 2. Get all attendance belonging to this student
    # --------------------------------------------------
    attendance_stmt = (
        db.select(
            Attendance.attendance_id,
            Attendance.attendance_date,
            Attendance.status,
            Enrolment.enrolment_id_bus,
            Course.course_id_bus,
            Course.course_name,
            Teacher.salutation,
            Teacher.first_name,
            Teacher.last_name,
        )
        .join(
            Enrolment,
            Attendance.enrolment_id == Enrolment.enrolment_id,
        )
        .join(
            Course,
            Enrolment.course_id == Course.course_id,
        )
        .join(
            Teacher,
            Course.teacher_id == Teacher.teacher_id,
        )
        .join(
            Users,
            Teacher.user_id == Users.user_id,
        )
        .where(Enrolment.student_id == student_internal_id)
        .order_by(Attendance.attendance_date.desc())
    )

    attendance_records = db.session.execute(attendance_stmt).all()

    return [
        {
            "attendance_id": record.attendance_id,
            "enrolment_id_bus": record.enrolment_id_bus,
            "course_id_bus": record.course_id_bus,
            "course_name": record.course_name,
            "attendance_date": record.attendance_date.isoformat(),
            "teacher": {"first_name": record.first_name, "last_name": record.last_name},
            "status": record.status,
        }
        for record in attendance_records
    ]
