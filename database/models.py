# from extensions import db

# integrate with /backend folder
from backend.app.extensions import db


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)

    # Keep for possible future Entra ID integration.
    # It can remain NULL while username/password authentication is used.
    entra_object_id = db.Column(db.String(255), nullable=True)

    email = db.Column(db.String(255), unique=True, nullable=False)

    role = db.Column(db.String(20), nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


class Student(db.Model):
    __tablename__ = "Student"

    student_id = db.Column(db.Integer, primary_key=True)

    student_id_bus = db.Column(db.String(20), unique=True, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("Users.user_id"), unique=True, nullable=False
    )

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    dob = db.Column(db.Date, nullable=True)

    mobile = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(20), nullable=False, default="ACTIVE", index=True)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('ACTIVE', 'INACTIVE')", name="ck_student_status"
        ),
    )


class Teacher(db.Model):
    __tablename__ = "Teacher"

    teacher_id = db.Column(db.Integer, primary_key=True)

    teacher_id_bus = db.Column(db.String(20), unique=True, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("Users.user_id"), unique=True, nullable=False
    )

    salutation = db.Column(db.String(10), nullable=True)

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    mobile = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(20), nullable=False, default="ACTIVE", index=True)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('ACTIVE', 'INACTIVE')", name="ck_teacher_status"
        ),
    )


class Admin(db.Model):
    __tablename__ = "Admin"

    admin_id = db.Column(db.Integer, primary_key=True)

    adm_id_bus = db.Column(db.String(20), unique=True, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("Users.user_id"), unique=True, nullable=False
    )

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    status = db.Column(db.String(20), nullable=False, default="ACTIVE", index=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    __table_args__ = (
        db.CheckConstraint("status IN ('ACTIVE', 'INACTIVE')", name="ck_admin_status"),
    )


class Classroom(db.Model):
    __tablename__ = "Classroom"

    classroom_id = db.Column(db.Integer, primary_key=True)

    room_name = db.Column(db.String(100), unique=True, nullable=False)

    class_capacity = db.Column(db.Integer, nullable=False)


class Course(db.Model):
    __tablename__ = "Course"

    course_id = db.Column(db.Integer, primary_key=True)

    course_id_bus = db.Column(db.String(20), unique=True, nullable=False)

    course_name = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=True)

    course_fee = db.Column(db.Numeric(10, 2), nullable=False)

    schedule = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)

    capacity = db.Column(db.Integer, nullable=False)

    teacher_id = db.Column(
        db.Integer, db.ForeignKey("Teacher.teacher_id"), nullable=False
    )

    classroom_id = db.Column(
        db.Integer, db.ForeignKey("Classroom.classroom_id"), nullable=False
    )
    teacher = db.relationship("Teacher")

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('OPEN', 'CLOSED', 'INACTIVE', 'PENDING')",
            name="ck_course_status",
        ),
    )


class Enrolment(db.Model):
    __tablename__ = "Enrolment"

    enrolment_id = db.Column(db.Integer, primary_key=True)

    enrolment_id_bus = db.Column(db.String(20), unique=True, nullable=False)

    student_id = db.Column(
        db.Integer, db.ForeignKey("Student.student_id"), nullable=False
    )

    course_id = db.Column(db.Integer, db.ForeignKey("Course.course_id"), nullable=False)

    # Hidaya requested a normal DATE rather than DateTime.
    enrolment_date = db.Column(
        db.Date, nullable=False, server_default=db.text("CAST(GETDATE() AS DATE)")
    )

    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name="uq_student_course"),
        db.CheckConstraint(
            "status IN ('PENDING', 'CONFIRMED', 'CANCELLED')",
            name="ck_enrolment_status",
        ),
    )


class Attendance(db.Model):
    __tablename__ = "Attendance"

    attendance_id = db.Column(db.Integer, primary_key=True)

    enrolment_id = db.Column(
        db.Integer, db.ForeignKey("Enrolment.enrolment_id"), nullable=False
    )

    attendance_date = db.Column(db.Date, nullable=False)

    # Teacher/backend must supply one of the three valid values.
    status = db.Column(db.String(20), nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint(
            "enrolment_id", "attendance_date", name="uq_attendance_enrolment_date"
        ),
        db.CheckConstraint(
            "status IN ('PRESENT', 'LATE', 'ABSENT')", name="ck_attendance_status"
        ),
    )


class Grade(db.Model):
    __tablename__ = "Grade"

    grade_id = db.Column(db.Integer, primary_key=True)

    enrolment_id = db.Column(
        db.Integer, db.ForeignKey("Enrolment.enrolment_id"), nullable=False
    )

    assessment_name = db.Column(db.String(150), nullable=False)

    score = db.Column(db.Numeric(5, 2), nullable=True)

    feedback = db.Column(db.Text, nullable=True)

    graded_date = db.Column(db.Date, nullable=True)
