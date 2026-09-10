from backend.app.extensions import db
from sqlalchemy.exc import IntegrityError

# Models
from database.models import Users, Student, Teacher, Admin

# Utils
from backend.app.utils.password import hash_password, verify_hash_password
from backend.app.utils import generate_business_id

# Exceptions
from backend.app.exceptions.auth import EmailAlreadyRegisteredError


def svc_register_student(data):

    # pre-check for duplicated email
    existing_student = Users.query.filter_by(email=data.email).first()

    if existing_student:
        raise EmailAlreadyRegisteredError("Email address is already registered.")

    try:
        # Create User
        user = Users(
            email=data.email,
            password_hash=hash_password(data.password),
            role="STUDENT",
        )

        db.session.add(user)
        db.session.flush()

        # Then create a Student record
        student = Student(
            student_id_bus=generate_business_id("STU"),
            first_name=data.first_name,
            last_name=data.last_name,
            mobile=data.mobile,
            dob=data.dob,
            user_id=user.user_id,
            status="ACTIVE",
        )

        db.session.add(student)

        db.session.commit()

        return user, student

    except IntegrityError:
        db.session.rollback()
        raise


def svc_update_student_profile(student_id_bus, update_data):
    student = Student.query.filter_by(student_id_bus=student_id_bus).first()

    if student is None:
        return None

    for field, value in update_data.items():
        setattr(student, field, value)

    db.session.commit()

    return student


def svc_register_teacher(data):

    # pre-check for duplicated email
    existing_user = Users.query.filter_by(email=data.email).first()

    if existing_user:
        raise EmailAlreadyRegisteredError("Email address is already registered.")

    try:
        # Create User
        user = Users(
            email=data.email,
            password_hash=hash_password(data.password),
            role="TEACHER",
        )

        db.session.add(user)
        db.session.flush()

        teacher = Teacher(
            teacher_id_bus=generate_business_id("TCH"),
            first_name=data.first_name,
            last_name=data.last_name,
            mobile=data.mobile,
            salutation=data.salutation,
            user_id=user.user_id,
            status="ACTIVE",
        )

        db.session.add(teacher)
        db.session.commit()

        return user, teacher

    except IntegrityError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise


def svc_update_teacher(teacher_id_bus, update_data):
    teacher = Teacher.query.filter_by(teacher_id_bus=teacher_id_bus).first()

    if teacher is None:
        return None

    for field, value in update_data.items():
        setattr(teacher, field, value)

    db.session.commit()

    return teacher


def svc_register_admin(data):

    # pre-check for duplicated email
    existing_user = Users.query.filter_by(email=data.email).first()

    if existing_user:
        raise EmailAlreadyRegisteredError("Email address is already registered.")

    try:
        # Create User
        user = Users(
            email=data.email,
            password_hash=hash_password(data.password),
            role="ADMIN",
        )

        db.session.add(user)
        db.session.flush()

        admin = Admin(
            first_name=data.first_name,
            last_name=data.last_name,
            user_id=user.user_id,
        )

        db.session.add(admin)
        db.session.commit()

        return user, admin

    except IntegrityError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise
