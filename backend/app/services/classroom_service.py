from app.extensions import db
from app.models.classroom import Classroom


def svc_create_classroom(data):
    classroom = Classroom(room_name=data.room_name, class_capacity=data.class_capacity)
    db.session.add(classroom)
    db.session.commit()

    return classroom
