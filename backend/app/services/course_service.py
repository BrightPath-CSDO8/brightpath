from backend.app.extensions import db

from database.models import Course

from backend.app.utils import generate_business_id


def svc_create_course(data):
    # Unique ID generation loop using modern 2.0 syntax
    # while True:
    #     generated_id = generate_business_id("CSR")

    #     # db.select() replaces Course.query
    #     # Builds the DB query:
    #     stmt = db.select(Course).where(Course.course_id_bus == generated_id)
    #     # Then send to DB, execute it and return the first scalar result
    #     existing_course = db.session.scalar(stmt)

    #     # If no collision is found, break out and use this ID
    #     if not existing_course:
    #         course_id_bus = generated_id
    #         break

    # # Instantiate the ORM object using consistent Pydantic dot notation
    # course = Course(
    #     course_id_bus=course_id_bus,
    #     course_name=data.course_name,
    #     course_fee=data.course_fee,
    #     description=data.description,
    #     schedule=data.schedule,
    #     start_date=data.start_date,
    #     end_date=data.end_date,
    #     capacity=data.capacity,
    #     status="PENDING",
    #     teacher_id=data.teacher_id,
    #     classroom_id=data.classroom_id,
    # )

    # db.session.add(course)
    # db.session.commit()

    # return course
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
        teacher_id=data["teacher_id"],
        classroom_id=data["classroom_id"],
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
