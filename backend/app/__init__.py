from flask import Flask
from backend.app.config import Config
from backend.app.extensions import db


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    app.secret_key = app.config["FLASK_SECRET_KEY"]  # Required for Flask sessions

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///edulearn.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Routes
    from backend.app.routes.auth import auth_bp
    from backend.app.routes.course import course_bp
    from backend.app.routes.classroom import classroom_bp

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(classroom_bp)

    return app
