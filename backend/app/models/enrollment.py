from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    enrolment_id_bus = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(
        db.Enum("CONFIRMED", "PENDING"),
        name="enrolment_status",
        nullable=False,
        default="PENDING",
        index=True,
    )
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "course_id", name="uniq_student_course_enrolment"
        ),
    )
