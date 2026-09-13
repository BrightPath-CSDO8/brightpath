from backend.app.extensions import db

from database.models import Users, Teacher, Student, Course, Enrolment

# Schema
from backend.app.schemas.teacher_schema import (
    TeacherCourse,
    CourseStudents,
    BulkAttendanceUpdate,
)

# Exceptions
from backend.app.exceptions.auth import (
    DuplicateError,
    NotFoundError,
    ForbiddenError,
)


def svc_teacher_courses(user_id: int) -> list[TeacherCourse]:
    stmt = (
        db.select(Teacher.teacher_id)
        .join(Users, Teacher.user_id == Users.user_id)
        .where(Users.user_id == user_id)
    )
    teacher_internal_id = db.session.scalar(stmt)

    if not teacher_internal_id:
        raise NotFoundError("Teacher is not in the system.")

    stmt_teacher_courses = db.select(Course).where(
        Course.teacher_id == teacher_internal_id
    )

    courses = db.session.scalars(stmt_teacher_courses).all()
    return [
        TeacherCourse(
            course_id_bus=course.course_id_bus,
            course_name=course.course_name,
            description=course.description,
            schedule=course.schedule,
            start_date=course.start_date,
            end_date=course.end_date,
            capacity=course.capacity,
            classroom_id=course.classroom_id,
            status=course.status,
        )
        for course in courses
    ]


def svc_teacher_students(user_id: str, course_id_bus: str) -> list[CourseStudents]:

    # obtain teacher's internal id
    teacher_stmt = (
        db.select(Teacher.teacher_id)
        .join(Users, Teacher.user_id == Users.user_id)
        .where(Users.user_id == user_id)
    )

    teacher_internal_id = db.session.scalar(teacher_stmt)

    if not teacher_internal_id:
        raise ForbiddenError("Current user is not a Teacher in the system.")

    # Check if courses is assigned to current teacher based on course_id_bus
    teacher_courses = db.select(Course.course_id).where(
        Course.teacher_id == teacher_internal_id, Course.course_id_bus == course_id_bus
    )
    course_internal_id = db.session.scalar(teacher_courses)

    if not course_internal_id:
        raise ForbiddenError("Teacher is not assigned to this course.")

    # Then obtain the students that are in that Course who are in "CONFIRMED" status
    students_enrolments_stmt = (
        db.select(Student, Enrolment.enrolment_id_bus)
        .join(Enrolment, Student.student_id == Enrolment.student_id)
        .where(
            Enrolment.course_id == course_internal_id, Enrolment.status == "CONFIRMED"
        )
    )
    confirmed_enrolments = db.session.execute(students_enrolments_stmt).all()
    if not confirmed_enrolments:
        return []

    return [
        CourseStudents(
            student_id_bus=student.student_id_bus,
            first_name=student.first_name,
            last_name=student.last_name,
            mobile=student.mobile,
            enrolment_id_bus=enrolment_id_bus,
        )
        for student, enrolment_id_bus in confirmed_enrolments
    ]


def svc_bulk_attendance(user_id: str, course_id_bus: str, data: BulkAttendanceUpdate):
    pass
