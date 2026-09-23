from backend.app.extensions import db

from database.models import Users, Teacher, Student, Course, Enrolment, Attendance

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
    ValidationError as AppValidationError,
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
    # --------------------------------------------------
    # 3. Get submitted enrolment business IDs
    # --------------------------------------------------
    submitted_enrolment_ids = [student.enrolment_id_bus for student in data.students]

    if not submitted_enrolment_ids:
        raise DuplicateError("At least one student attendance record is required.")

    if len(submitted_enrolment_ids) != len(set(submitted_enrolment_ids)):
        raise DuplicateError("Duplicate enrolment IDs are not allowed.")

    # --------------------------------------------------
    # 4. Resolve enrolments belonging to this course
    # --------------------------------------------------
    enrolment_stmt = db.select(
        Enrolment.enrolment_id,
        Enrolment.enrolment_id_bus,
    ).where(
        Enrolment.course_id == course_internal_id,
        Enrolment.enrolment_id_bus.in_(submitted_enrolment_ids),
    )

    enrolments = db.session.execute(enrolment_stmt).all()

    # Map:
    # enrolment_id_bus -> internal enrolment_id
    enrolment_map = {
        enrolment.enrolment_id_bus: enrolment.enrolment_id for enrolment in enrolments
    }

    # --------------------------------------------------
    # 5. Check for invalid enrolments
    # --------------------------------------------------
    missing_enrolments = [
        enrolment_id_bus
        for enrolment_id_bus in submitted_enrolment_ids
        if enrolment_id_bus not in enrolment_map
    ]

    if missing_enrolments:
        raise AppValidationError(
            f"Invalid enrolment(s) for this course: " f"{', '.join(missing_enrolments)}"
        )

    # --------------------------------------------------
    # 6. Find existing attendance records for this date
    # --------------------------------------------------
    internal_enrolment_ids = list(enrolment_map.values())

    attendance_stmt = db.select(Attendance).where(
        Attendance.enrolment_id.in_(internal_enrolment_ids),
        Attendance.attendance_date == data.attendance_date,
    )

    existing_attendance = db.session.execute(attendance_stmt).scalars().all()

    # Map:
    # internal enrolment_id -> Attendance object
    attendance_map = {
        attendance.enrolment_id: attendance for attendance in existing_attendance
    }

    # --------------------------------------------------
    # 7. Insert or update attendance
    # --------------------------------------------------
    created = 0
    updated = 0

    try:
        for student in data.students:

            enrolment_internal_id = enrolment_map[student.enrolment_id_bus]

            attendance = attendance_map.get(enrolment_internal_id)

            if attendance:
                # Existing attendance -> UPDATE
                attendance.status = student.status.value
                updated += 1

            else:
                # No attendance yet -> INSERT
                attendance = Attendance(
                    enrolment_id=enrolment_internal_id,
                    attendance_date=data.attendance_date,
                    status=student.status.value,
                )

                db.session.add(attendance)
                # Keep the map synchronized
                attendance_map[enrolment_internal_id] = attendance

                created += 1

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "message": "Attendance submitted successfully.",
        "attendance_date": data.attendance_date.isoformat(),
        "created": created,
        "updated": updated,
        "total": len(data.students),
    }
