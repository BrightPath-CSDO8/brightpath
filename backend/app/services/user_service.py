# Handles Business Logics

from app.extensions import db
from app.models.users import User, Student
from sqlalchemy.exc import IntegrityError

# Utils
from app.utils.password import hash_password, verify_hash_password
from app.utils import generate_business_id

# Exceptions
from app.exceptions.auth import EmailAlreadyRegisteredError


def svc_register_student(data, identity):

    # Extract identity information
    entra_object_id = identity["oid"]
    email = identity["email"]

    # pre-check for duplicated email
    existing_user = User.query.filter_by(email=email).first()
    # When Entra iD is implemented:
    # existing_user = User.query.filter_by(entra_object_id=entra_object_id).first()

    if existing_user:
        raise EmailAlreadyRegisteredError("Email address is already registered.")

    try:
        # Create User
        user = User(
            email=email,
            entra_object_id=entra_object_id,
            # password_hash=hash_password(data.password),
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
