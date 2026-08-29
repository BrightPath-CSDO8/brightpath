from app.extensions import db
from app.models.course import Course

from app.utils import generate_business_id


def svc_create_course(data):

    while True:
        course_id_bus = generate_business_id("CSR")

        existing_course_id = Course.query.filter_by(course_id_bus=course_id_bus).first()

        if not existing_course_id:
            break

    course = Course(
        course_id_bus=course_id_bus,
        course_name=data["course_name"],
        course_fee=data["course_fee"],
        description=data["description"],
        schedule=data["schedule"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        capacity=data["capacity"],
        status="PENDING",
    )

    db.session.add(course)
    db.session.commit()

    return course


def svc_update_course(course_id_bus, update_data):
    course = Course.query.filter_by(course_id_bus=course_id_bus).first()

    if course is None:
        return None

    for field, value in update_data.items():
        setattr(course, field, value)

    db.session.commit()

    return course
