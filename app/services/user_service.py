from app.extensions import db
from app.models.users import User

# Utils
from app.utils.password import hash_password, verify_hash_password


def svc_register_student(data):
    print(f"STudent creation: {data}")
    user = User(
        email=data["email"],
        password_hash=hash_password(data["password"]),
        role="STUDENT",
    )

    db.session.add(user)
    db.session.commit()

    return user


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
