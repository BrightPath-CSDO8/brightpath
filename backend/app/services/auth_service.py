from backend.app.extensions import db
from database.models import Users, Student, Teacher

# Utils
from backend.app.utils.password import verify_hash_password

# Exceptions
from backend.app.exceptions.auth import AuthenticationError


def svc_login(data):
    user = Users.query.filter_by(email=data.email).first()

    if not user:
        raise AuthenticationError("Invalid email and/or password.")

    verified_password = verify_hash_password(data.password, user.password_hash)

    if not verified_password:
        raise AuthenticationError("Invalid email and/or password.")

    # Student profile lookup
    if user.role == "STUDENT":
        student = Student.query.filter_by(user_id=user.user_id).first()

        if not student:
            raise AuthenticationError("Student profile not found.")
        return user, student

    # Teacher profile lookup

    # if user.role == "TEACHER":
    #     teacher = Teacher.query.filter_by(user_id=user.user_id).first()

    #     if not teacher:
    #         raise AuthenticationError("Teacher profile not found.")
    #     return user, None, teacher

    return user, student
