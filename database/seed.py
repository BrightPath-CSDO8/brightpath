from backend.app.extensions import db
from backend.app.utils.password import hash_password
from database.models import (
    Users,
    Student,
    Teacher,
    Admin,
    Classroom,
    Course,
    Enrolment,
    Attendance,
    Grade,
)
from datetime import date

# Utils


def seed_database():
    # --------------------------------------------------
    # Users
    # --------------------------------------------------

    teacher_user = Users(
        entra_object_id=None,
        email="teacher-dev@example.com",
        role="TEACHER",
        password_hash=hash_password("teacher123"),
    )

    student_user = Users(
        entra_object_id=None,
        email="student-dev@example.com",
        role="STUDENT",
        password_hash=hash_password("student123"),
    )

    admin_user = Users(
        entra_object_id=None,
        email="admin-dev@example.com",
        role="ADMIN",
        password_hash=hash_password("admin123"),
    )

    db.session.add_all(
        [
            teacher_user,
            student_user,
            admin_user,
        ]
    )

    db.session.flush()

    # --------------------------------------------------
    # Teacher
    # --------------------------------------------------

    teacher = Teacher(
        teacher_id_bus="TCH-0001",
        user_id=teacher_user.user_id,
        salutation="Ms",
        first_name="Alice",
        last_name="Tan",
        mobile="98765432",
        status="ACTIVE",
    )

    # --------------------------------------------------
    # Student
    # --------------------------------------------------

    student = Student(
        student_id_bus="STU-0001",
        user_id=student_user.user_id,
        first_name="Bob",
        last_name="Lim",
        dob=date.fromisoformat("2000-05-15"),
        mobile="91234567",
        status="ACTIVE",
    )

    # --------------------------------------------------
    # Admin
    # --------------------------------------------------

    admin = Admin(
        user_id=admin_user.user_id,
        first_name="Charlie",
        last_name="Lee",
    )

    db.session.add_all(
        [
            teacher,
            student,
            admin,
        ]
    )

    db.session.flush()

    # --------------------------------------------------
    # Classrooms
    # --------------------------------------------------

    classroom1 = Classroom(
        room_name="Roses",
        class_capacity=20,
    )

    classroom2 = Classroom(
        room_name="Daisies",
        class_capacity=30,
    )

    classroom3 = Classroom(
        room_name="Tulips",
        class_capacity=40,
    )

    db.session.add_all(
        [
            classroom1,
            classroom2,
            classroom3,
        ]
    )

    db.session.flush()

    # --------------------------------------------------
    # Courses
    # --------------------------------------------------

    course1 = Course(
        course_id_bus="CSR-1010",
        course_name="Python Fundamentals",
        course_fee=180.80,
        description="Learn the basics of Python.",
        schedule="Monday 9am - 11am",
        start_date=date.fromisoformat("2026-09-15"),
        end_date=date.fromisoformat("2026-10-15"),
        status="OPEN",
        capacity=20,
        teacher_id=teacher.teacher_id,
        classroom_id=classroom1.classroom_id,
    )

    course2 = Course(
        course_id_bus="CSR-1011",
        course_name="Introduction to Computer Science",
        course_fee=180.80,
        description="An introductory computer science course.",
        schedule="Tuesday 9am - 11am",
        start_date=date.fromisoformat("2026-10-20"),
        end_date=date.fromisoformat("2026-11-20"),
        status="PENDING",
        capacity=25,
        teacher_id=teacher.teacher_id,
        classroom_id=classroom2.classroom_id,
    )

    course3 = Course(
        course_id_bus="CSR-1012",
        course_name="Introduction to Cloud Infrastructure",
        course_fee=300.80,
        description="Learn the fundamentals of cloud infrastructure.",
        schedule="Wednesday 7pm - 9pm",
        start_date=date.fromisoformat("2026-11-01"),
        end_date=date.fromisoformat("2026-12-01"),
        status="OPEN",
        capacity=30,
        teacher_id=teacher.teacher_id,
        classroom_id=classroom3.classroom_id,
    )

    db.session.add_all(
        [
            course1,
            course2,
            course3,
        ]
    )

    db.session.flush()

    # --------------------------------------------------
    # Enrolment
    # --------------------------------------------------

    enrolment = Enrolment(
        enrolment_id_bus="ENR-0001",
        student_id=student.student_id,
        course_id=course1.course_id,
        status="APPROVED",
    )

    db.session.add(enrolment)

    db.session.flush()

    # --------------------------------------------------
    # Attendance
    # --------------------------------------------------

    attendance = Attendance(
        enrolment_id=enrolment.enrolment_id,
        attendance_date=date.fromisoformat("2026-09-15"),
        status="PRESENT",
    )

    db.session.add(attendance)

    # --------------------------------------------------
    # Grade
    # --------------------------------------------------

    grade = Grade(
        enrolment_id=enrolment.enrolment_id,
        assessment_name="Python Fundamentals Assessment",
        score=85.50,
        feedback="Good understanding of the fundamentals.",
        graded_date=date.fromisoformat("2026-09-20"),
    )

    db.session.add(grade)

    # --------------------------------------------------
    # Commit everything
    # --------------------------------------------------

    db.session.commit()

    print("Database seeded successfully.")
