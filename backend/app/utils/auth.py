from functools import wraps

from flask import jsonify, session


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

        return view(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            user_role = session.get("role")

            if not user_role:
                return (
                    jsonify(
                        {
                            "error": "Unauthorized.",
                            "message": "Authentication required.",
                        }
                    ),
                    401,
                )

            if user_role not in allowed_roles:
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
