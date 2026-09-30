from functools import wraps

from flask import jsonify, session, g
from backend.app.extensions import db
from database.models import Users, Student, Teacher, Admin

from backend.app.exceptions.auth import ForbiddenError


def get_user_profile(current_user):

    if current_user.role == "STUDENT":
        return db.session.scalar(
            db.select(Student).where(Student.user_id == current_user.user_id)
        )

    if current_user.role == "TEACHER":
        return db.session.scalar(
            db.select(Teacher).where(Teacher.user_id == current_user.user_id)
        )

    if current_user.role == "ADMIN":
        return db.session.scalar(
            db.select(Admin).where(Admin.user_id == current_user.user_id)
        )

    return None


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get("user_id")

        if not user_id:
            return (
                jsonify(
                    {
                        "error": "Unauthorized.",
                        "message": "Authentication required.",
                    }
                ),
                401,
            )

        current_user = db.session.get(Users, user_id)

        if current_user is None:
            session.clear()
            return (
                jsonify(
                    {
                        "error": "Unauthorized.",
                        "message": "User account not found.",
                    }
                ),
                401,
            )

        current_user_profile = get_user_profile(current_user)

        if current_user_profile.status == "INACTIVE":
            # session.clear()
            return (
                jsonify(
                    {
                        "error": "Forbidden.",
                        "message": "Account is inactive. Contact Administrator.",
                    }
                ),
                403,
            )

        g.current_user = current_user
        g.current_user_profile = current_user_profile

        return view(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            current_user = g.current_user

            if current_user.role not in allowed_roles:
                return (
                    jsonify(
                        {
                            "error": "Forbidden.",
                            "message": "You do not have permission to access this resource.",
                        }
                    ),
                    403,
                )

            return view(*args, **kwargs)

        return wrapped_view

    return decorator


def get_current_user():
    return g.current_user


def authorize_student_access(student):

    current_user = get_current_user()

    if current_user.role == "ADMIN":
        return

    if student.user_id != current_user.user_id:
        raise ForbiddenError("You are not allowed to modify this profile.")


def authorize_teacher_access(teacher):

    current_user = get_current_user()

    if current_user.role == "ADMIN":
        return

    if teacher.user_id != current_user.user_id:
        raise ForbiddenError("You are not allowed to modify this profile.")
