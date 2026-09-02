from flask import Flask
from app.extensions import db
from datetime import date


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///edulearn.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Models
    from app.models.course import Course

    # Routes
    from app.routes.course import course_bp
    from app.routes.auth import auth_bp

    # from . import models

    with app.app_context():
        db.create_all()

        if Course.query.count() == 0:
            course1 = Course(
                course_id_bus="CSR-1010",
                course_name="Python Fundamentals",
                course_fee=180.80,
                description="Learn the basics of Python",
                schedule="Monday 9am - 11am",
                start_date=date.fromisoformat("2026-04-10"),
                end_date=date.fromisoformat("2026-05-01"),
                capacity=20,
                status="OPEN",
            )
            course2 = Course(
                course_id_bus="CSR-1011",
                course_name="Introduction to Computer Science",
                course_fee=180.80,
                description="An introductory computer science course.",
                schedule="Tuesday 9am - 11am",
                start_date=date.fromisoformat("2026-07-10"),
                end_date=date.fromisoformat("2026-08-13"),
                capacity=20,
                status="PENDING",
            )
            course3 = Course(
                course_id_bus="CSR-1013",
                course_name="Introduction to Cloud Infrastructure with AWS",
                course_fee=300.80,
                description="Learn how to build and manage modern web apps in the cloud. This beginner course covers core Amazon Web Services tools like EC2 servers, S3 storage, and basic networking. You will deploy your first live application by the end of the class. No prior cloud experience is needed.",
                schedule="Tuesday 9am - 11am",
                start_date=date.fromisoformat("2026-09-10"),
                end_date=date.fromisoformat("2026-10-01"),
                capacity=30,
                status="OPEN",
            )
            course4 = Course(
                course_id_bus="CSR-2020",
                course_name="Introduction to Web Application",
                course_fee=280.80,
                description="An introductory computer science course.",
                schedule="Tuesday 9am - 11am",
                start_date=date.fromisoformat("2026-08-10"),
                end_date=date.fromisoformat("2026-09-01"),
                capacity=40,
                status="INACTIVE",
            )
            db.session.add_all([course1, course2, course3, course4])

            db.session.commit()

    app.register_blueprint(course_bp)
    app.register_blueprint(auth_bp)

    return app
