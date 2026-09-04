from app.extensions import db
from app.models.users import User, Student

# Utils
from app.utils.password import verify_hash_password

# Exceptions
from app.exceptions.auth import AuthenticationError


def svc_login(data):
    user = User.query.filter_by(email=data.email).first()

    if not user:
        raise AuthenticationError("Invalid email and/or password.")

    verified_password = verify_hash_password(data.password, user.password_hash)

    if not verified_password:
        raise AuthenticationError("Invalid email and/or password.")

    return user
