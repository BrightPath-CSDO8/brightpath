from backend.app.extensions import db
from database.models import Users, Student, Teacher, Admin

# Utils
from backend.app.utils.password import hash_password, verify_hash_password

from database.models import Users

# Exceptions
from backend.app.exceptions.auth import (
    AuthenticationError,
    ForbiddenError,
    ValidationError as AppValidationError,
)


def get_user_profile(user):
    if user.role == "STUDENT":
        user_profile = Student.query.filter_by(user_id=user.user_id).first()

        if not user_profile:
            raise AuthenticationError("Student profile not found.")

        if user_profile.status == "INACTIVE":
            raise ForbiddenError("Account inactive. Contact Administrator.")

    elif user.role == "TEACHER":
        user_profile = Teacher.query.filter_by(user_id=user.user_id).first()
        if not user_profile:
            raise AuthenticationError("Teacher profile not found.")
        if user_profile.status == "INACTIVE":
            raise ForbiddenError("Account inactive. Contact Administrator.")

    elif user.role == "ADMIN":
        user_profile = Admin.query.filter_by(user_id=user.user_id).first()
        if not user_profile:
            raise AuthenticationError("Admin profile not found.")
        if user_profile.status == "INACTIVE":
            raise ForbiddenError("Account inactive. Contact Administrator.")

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


def svc_change_password(user_id, data):
    user = db.session.scalar(db.select(Users).where(Users.user_id == user_id))

    if not user:
        raise AuthenticationError("User account not found.")

    if not verify_hash_password(
        data.current_password,
        user.password_hash,
    ):
        raise AppValidationError("Incorrect account password.")

    if data.new_password != data.confirm_password:
        raise AppValidationError("New password and confirm password do not match.")

    if verify_hash_password(
        data.new_password,
        user.password_hash,
    ):
        raise AppValidationError("Old password cannot be reused.")

    user.password_hash = hash_password(data.new_password)

    db.session.commit()
