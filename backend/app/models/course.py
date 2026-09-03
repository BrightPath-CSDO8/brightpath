from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_id_bus = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    course_fee = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    schedule = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(
        db.Enum("OPEN", "CLOSED", "INACTIVE", "PENDING"),
        name="course_status_enum",
        index=True,
    )
    capacity = db.Column(db.Integer)
