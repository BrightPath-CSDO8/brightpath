from backend.app.extensions import db

from database.models import Users, Student, Course, Enrolment

from backend.app.utils import generate_business_id

# Schema
from backend.app.schemas.enrolment_schema import (
    EnrolmentCreate,
    EnrolmentCreateResponse,
    StudentAllEnrolments,
    AdminAllEnrolments,
    AdminUpdateEnrolment,
)
from backend.app.schemas.user_schema import StudentProfile

from backend.app.exceptions.auth import (
    DuplicateError,
    NotFoundError,
    ForbiddenError,
)


def svc_create_enrolment(
    data: EnrolmentCreate, user_id: int
) -> EnrolmentCreateResponse:

    # We JOIN Student onto Users to extract Student.student_id directly using user_id
    student_stmt = (
        db.select(Student)
        .join(
            Users, Student.user_id == Users.user_id
        )  # links your student profile to user account
        .where(Users.user_id == user_id)
    )
    student = db.session.scalar(student_stmt)
    if not student:
        raise ForbiddenError("You do not have access to this resource.")

    # Checks Course exists AND status = "OPEN"
    course_stmt = db.select(Course.course_id).where(
        Course.course_id_bus == data["course_id_bus"], Course.status == "OPEN"
    )
    internal_course_id = db.session.scalar(course_stmt)

    if not internal_course_id:
        raise NotFoundError("Course is not available for enrolment.")

    # Check if student has already enrol in this particular course:
    enrolment_stmt = db.select(Enrolment).where(
        Enrolment.student_id == student.student_id,
        Enrolment.course_id == internal_course_id,
    )
    enrolment_found = db.session.scalar(enrolment_stmt)

    if enrolment_found:
        raise DuplicateError("Student has already registered for course.")

    new_enrolment = Enrolment(
        enrolment_id_bus=generate_business_id("ENR"),
        student_id=student.student_id,
        course_id=internal_course_id,
        status="PENDING",
    )

    db.session.add(new_enrolment)
    db.session.commit()

    return EnrolmentCreateResponse(
        # student=StudentProfile.model_validate(student),
        enrolment_id_bus=new_enrolment.enrolment_id_bus,
        status=new_enrolment.status,
    )


def svc_student_enrolments(
    user_id: int, status: str = None
) -> list[StudentAllEnrolments]:
    student_stmt = (
        db.select(Student.student_id)
        .join(Users, Student.user_id == Users.user_id)
        .where(Users.user_id == user_id)
    )

    student_internal_id = db.session.scalar(student_stmt)

    if not student_internal_id:
        raise ForbiddenError(
            "Current user is not registered as a student in this system."
        )

    # Get all enrolments belonging to this student
    student_enrolments_stmt = (
        db.select(Enrolment, Course)
        .join(Course, Enrolment.course_id == Course.course_id)
        .where(Enrolment.student_id == student_internal_id)
    )
    if status:
        student_enrolments_stmt = (
            db.select(Enrolment, Course)
            .join(Course, Enrolment.course_id == Course.course_id)
            .where(Enrolment.student_id == student_internal_id)
            .where(Enrolment.status == status.upper())
        )

    results = db.session.execute(student_enrolments_stmt).all()

    return [
        StudentAllEnrolments(
            enrolment_id_bus=enrolment.enrolment_id_bus,
            course_id_bus=course.course_id_bus,
            course_name=course.course_name,
            start_date=course.start_date,
            end_date=course.end_date,
            enrolment_date=enrolment.enrolment_date,
            status=enrolment.status,
        )
        for enrolment, course in results
    ]


def svc_admin_enrolments(status: str = None) -> list[AdminAllEnrolments]:
    stmt = (
        db.select(
            Enrolment.enrolment_id_bus,
            Student.student_id_bus,
            Student.first_name,
            Student.last_name,
            Course.course_id_bus,
            Course.course_name,
            Enrolment.status,
        )
        .join(Student, Enrolment.student_id == Student.student_id)
        .join(Course, Enrolment.course_id == Course.course_id)
    )

    if status:
        stmt = stmt.where(Enrolment.status == status.upper())

    results = db.session.execute(stmt).mappings().all()
    return [AdminAllEnrolments.model_validate(row).model_dump() for row in results]


def svc_admin_update_enrolment(
    enrolment_id_bus: str,
    data: AdminUpdateEnrolment,
) -> Enrolment:

    stmt = db.select(Enrolment).where(Enrolment.enrolment_id_bus == enrolment_id_bus)

    enrolment = db.session.scalar(stmt)

    if not enrolment:
        raise NotFoundError("Enrolment is not registered.")

    enrolment.status = data.status.value

    db.session.commit()

    return enrolment
