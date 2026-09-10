from backend.app.extensions import db
from database.models import Users, Student, Teacher, Admin

# Utils
from backend.app.utils.password import verify_hash_password

# Exceptions
from backend.app.exceptions.auth import AuthenticationError


def get_user_profile(user):
    if user.role == "STUDENT":
        user_profile = Student.query.filter_by(user_id=user.user_id).first()

        if not user_profile:
            raise AuthenticationError("Student profile not found.")

    elif user.role == "TEACHER":
        user_profile = Teacher.query.filter_by(user_id=user.user_id).first()
        if not user_profile:
            raise AuthenticationError("Teacher profile not found.")

    elif user.role == "ADMIN":
        user_profile = Admin.query.filter_by(user_id=user.user_id).first()
        if not user_profile:
            raise AuthenticationError("Admin profile not found.")
    else:
        raise AuthenticationError("Invalid user role.")
    return user_profile


def svc_login(data):
    user = Users.query.filter_by(email=data.email).first()

    if not user:
        raise AuthenticationError("Invalid email and/or password.")

    verified_password = verify_hash_password(data.password, user.password_hash)

    if not verified_password:
        raise AuthenticationError("Invalid email and/or password.")

    user_profile = get_user_profile(user)

    return user, user_profile


def svc_me(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        raise AuthenticationError("User account not found.")

    user_profile = get_user_profile(user)

    return user, user_profile
