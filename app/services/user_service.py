# Handles Business Logics

from app.extensions import db
from app.models.users import User, Student
from sqlalchemy.exc import IntegrityError

# Utils
from app.utils.password import hash_password, verify_hash_password
from app.utils import generate_business_id

# Exceptions
from app.exceptions.auth import EmailAlreadyRegisteredError


def svc_register_student(data):

    # pre-check for duplicated email
    existing_student = User.query.filter_by(email=data.email).first()

    if existing_student:
        raise EmailAlreadyRegisteredError("Email address is already registered.")

    try:
        # Create User
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role="STUDENT",
        )

        # Then create a Student record
        student = Student(
            student_id_bus=generate_business_id("STU"),
            first_name=data.first_name,
            last_name=data.last_name,
            mobile=data.mobile,
            dob=data.dob,
            user=user,
        )

        db.session.add(user)
        db.session.add(student)

        db.session.commit()

        return student

    except IntegrityError:
        db.session.rollback()
        raise


def svc_register_staff(data):
    print(f"Staff data: {data}")
    user = User(
        email=data["email"],
        password_hash=data["password_hash"],
        role=data["target_role"],
    )

    db.session.add(user)
    db.session.commit()

    return user
