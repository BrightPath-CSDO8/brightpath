from app.extensions import db
from app.models.course import Course


def svc_update_course(course_id_bus, update_data):
    course = Course.query.filter_by(course_id_bus=course_id_bus).first()

    if course is None:
        return None

    for field, value in update_data.items():
        setattr(course, field, value)

    db.session.commit()

    return course
