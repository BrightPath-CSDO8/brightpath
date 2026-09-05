from app.models.users import User, Student
from app.exceptions.auth import AuthenticationError

# This Auth Service to meant to check Authentication from Entra ID.


def resolve_student(identity):
    user = User.query.filter_by(entra_object_id=identity.entra_object_id).first()

    if not user:
        raise AuthenticationError("User is authenticated but does not have an account.")

    # if user.role != "STUDENT":
    #     raise AuthenticationError("User is not registered as a student.")

    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        raise AuthenticationError("Student profile does not exist.")

    return {
        "user_id": user.id,
        "student_id_bus": student.student_id_bus,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "dob": student.dob,
    }
