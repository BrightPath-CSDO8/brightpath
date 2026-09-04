from app.extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(
        db.Enum("SUPERADMIN", "ADMIN", "STUDENT", "TEACHER"),
        name="user_role",
        nullable=False,
    )
    # Temporary nullable=True, to be change to False once Entra ID is ready
    entra_object_id = db.Column(db.String(255), unique=True, nullable=True)
    # password_hash is irrelevant once Entra ID is implemented
    password_hash = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Singapore")),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Singapore")),
        onupdate=lambda: datetime.now(ZoneInfo("Asia/Singapore")),
    )
    student = db.relationship("Student", back_populates="user", uselist=False)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )
    student_id_bus = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.Date)
    mobile = db.Column(db.String(20))

    user = db.relationship("User", back_populates="student")
