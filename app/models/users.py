from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(
        db.Enum("SUPERADMIN", "ADMIN", "STUDENT", "TEACHER"),
        name="user_role",
        nullable=False,
    )
    # created_at = db.Column(db.DateTime, nullable=False)
    # Temporary nullable=True, to be replaced with Entra ID
    entra_object_id = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
