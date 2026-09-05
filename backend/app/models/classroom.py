from app.extensions import db


class Classroom(db.Model):
    __tablename__ = "classroom"

    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(
        db.String(20),
        index=True,
        nullable=False,
    )
    class_capacity = db.Column(db.Integer)

    courses = db.relationship("Course", back_populates="classroom")
