from app.extensions import db

# Models
from app.models.course import Course
from app.models.users import Student
from backend.app.models.enrollment import Enrollment

# Utils
from app.utils import generate_business_id


def svc_student_enrol(data):

    course = Course.query.filter_by(course_id_bus=data.course_id_bus)

    if not course:
        return "404. Course not found"

    if course.status is not "OPEN":
        return "Course not available."

    enrolment = Enrollment(
        enrolment_id_bus=generate_business_id("ENR"),
        status="PENDING",
        student_id_bus="",
        course_id_bus="",
    )

    db.session.add(enrolment)
    db.session.commit()

    return enrolment
