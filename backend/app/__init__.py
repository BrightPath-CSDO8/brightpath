from flask import Flask
from backend.app.config import Config
from backend.app.extensions import db


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    app.secret_key = app.config["FLASK_SECRET_KEY"]  # Required for Flask sessions

    # initialized SQLAlchemy
    db.init_app(app)

    # Routes
    from backend.app.routes.auth import auth_bp
    from backend.app.routes.course import course_bp
    from backend.app.routes.classroom import classroom_bp
    from backend.app.routes.teacher import teacher_bp
    from backend.app.routes.student import student_bp
    from backend.app.routes.admin import admin_bp
    from backend.app.routes.enrolment import enrol_bp

    # with app.app_context():
    #     db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(classroom_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(enrol_bp)

    return app
