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


def svc_student_grades(user_id: int):
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
    # 2. Get all grades belonging to this student
    # --------------------------------------------------
    grade_stmt = (
        db.select(
            Grade.grade_id,
            Grade.assessment_name,
            Grade.score,
            Grade.feedback,
            Grade.graded_date,
            Enrolment.enrolment_id_bus,
            Course.course_id_bus,
            Course.course_name,
            Teacher.first_name,
            Teacher.last_name,
        )
        .join(
            Enrolment,
            Grade.enrolment_id == Enrolment.enrolment_id,
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
        .order_by(Grade.graded_date.desc())
    )

    grade_records = db.session.execute(grade_stmt).all()

    return {
        "total": len(grade_records),
        "grades": [
            {
                # "grade_id": record.grade_id,
                "enrolment_id_bus": record.enrolment_id_bus,
                "course": {
                    "course_id_bus": record.course_id_bus,
                    "course_name": record.course_name,
                },
                "teacher": {
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                },
                "assessment_name": record.assessment_name,
                "score": float(record.score) if record.score is not None else None,
                "feedback": record.feedback,
                "graded_date": (
                    record.graded_date.isoformat() if record.graded_date else None
                ),
            }
            for record in grade_records
        ],
    }
