from backend.app.extensions import db

# from app.models.users import User, Student
from database.models import Users, Student

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

    return user
