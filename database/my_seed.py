from datetime import date

from werkzeug.security import generate_password_hash

from database.app import app
from backend.app.extensions import db
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


def seed_database():

    # --------------------------------------------------
    # Users
    # --------------------------------------------------

    teacher_user1 = Users(
        entra_object_id=None,
        email="alice.tan@example.com",
        role="TEACHER",
        password_hash=generate_password_hash("Teacher123!"),
    )

    teacher_user2 = Users(
        entra_object_id=None,
        email="daniel.lim@example.com",
        role="TEACHER",
        password_hash=generate_password_hash("Teacher123!"),
    )

    student_user1 = Users(
        entra_object_id=None,
        email="ethan.lee@example.com",
        role="STUDENT",
        password_hash=generate_password_hash("Student123!"),
    )

    student_user2 = Users(
        entra_object_id=None,
        email="chloe.tan@example.com",
        role="STUDENT",
        password_hash=generate_password_hash("Student123!"),
    )

    student_user3 = Users(
        entra_object_id=None,
        email="ryan.wong@example.com",
        role="STUDENT",
        password_hash=generate_password_hash("Student123!"),
    )

    student_user4 = Users(
        entra_object_id=None,
        email="sarah.lim@example.com",
        role="STUDENT",
        password_hash=generate_password_hash("Student123!"),
    )

    admin_user = Users(
        entra_object_id=None,
        email="michelle.koh@example.com",
        role="ADMIN",
        password_hash=generate_password_hash("Admin123!"),
    )

    db.session.add_all([
        teacher_user1,
        teacher_user2,
        student_user1,
        student_user2,
        student_user3,
        student_user4,
        admin_user,
    ])

    # SQL Server generates the internal user_id values.
    db.session.flush()

    # --------------------------------------------------
    # Teachers
    # --------------------------------------------------

    teacher1 = Teacher(
        teacher_id_bus="TCH-0001",
        user_id=teacher_user1.user_id,
        salutation="Ms",
        first_name="Alice",
        last_name="Tan",
        mobile="81234567",
        status="ACTIVE",
    )

    teacher2 = Teacher(
        teacher_id_bus="TCH-0002",
        user_id=teacher_user2.user_id,
        salutation="Mr",
        first_name="Daniel",
        last_name="Lim",
        mobile="82345678",
        status="ACTIVE",
    )

    # --------------------------------------------------
    # Students
    # --------------------------------------------------

    student1 = Student(
        student_id_bus="STU-0001",
        user_id=student_user1.user_id,
        first_name="Ethan",
        last_name="Lee",
        dob=date.fromisoformat("2002-03-15"),
        mobile="83456789",
        status="ACTIVE",
    )

    student2 = Student(
        student_id_bus="STU-0002",
        user_id=student_user2.user_id,
        first_name="Chloe",
        last_name="Tan",
        dob=date.fromisoformat("2001-07-22"),
        mobile="84567890",
        status="ACTIVE",
    )

    student3 = Student(
        student_id_bus="STU-0003",
        user_id=student_user3.user_id,
        first_name="Ryan",
        last_name="Wong",
        dob=date.fromisoformat("2003-01-10"),
        mobile="85678901",
        status="ACTIVE",
    )

    student4 = Student(
        student_id_bus="STU-0004",
        user_id=student_user4.user_id,
        first_name="Sarah",
        last_name="Lim",
        dob=date.fromisoformat("2002-11-05"),
        mobile="86789012",
        status="ACTIVE",
    )

    # --------------------------------------------------
    # Admin
    # --------------------------------------------------

    admin = Admin(
        adm_id_bus="ADM-0001",
        user_id=admin_user.user_id,
        first_name="Michelle",
        last_name="Koh",
        status="ACTIVE",
    )

    db.session.add_all([
        teacher1,
        teacher2,
        student1,
        student2,
        student3,
        student4,
        admin,
    ])

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

    db.session.add_all([
        classroom1,
        classroom2,
        classroom3,
    ])

    db.session.flush()

    # --------------------------------------------------
    # Courses
    # --------------------------------------------------

    course1 = Course(
        course_id_bus="CSR-1010",
        course_name="Python Fundamentals",
        course_fee=180.80,
        description="Learn the basics of Python programming.",
        schedule="Monday 9am - 11am",
        start_date=date.fromisoformat("2026-09-15"),
        end_date=date.fromisoformat("2026-10-15"),
        status="OPEN",
        capacity=20,
        teacher_id=teacher1.teacher_id,
        classroom_id=classroom1.classroom_id,
    )

    course2 = Course(
        course_id_bus="CSR-1011",
        course_name="Introduction to Computer Science",
        course_fee=180.80,
        description="An introductory course covering core computer science concepts.",
        schedule="Tuesday 9am - 11am",
        start_date=date.fromisoformat("2026-10-20"),
        end_date=date.fromisoformat("2026-11-20"),
        status="PENDING",
        capacity=25,
        teacher_id=teacher2.teacher_id,
        classroom_id=classroom2.classroom_id,
    )

    course3 = Course(
        course_id_bus="CSR-1012",
        course_name="Introduction to Cloud Infrastructure",
        course_fee=300.80,
        description="Learn the fundamentals of cloud infrastructure and services.",
        schedule="Wednesday 7pm - 9pm",
        start_date=date.fromisoformat("2026-11-01"),
        end_date=date.fromisoformat("2026-12-01"),
        status="OPEN",
        capacity=30,
        teacher_id=teacher1.teacher_id,
        classroom_id=classroom3.classroom_id,
    )

    db.session.add_all([
        course1,
        course2,
        course3,
    ])

    db.session.flush()

    # --------------------------------------------------
    # Enrolments
    # --------------------------------------------------

    enrolment1 = Enrolment(
        enrolment_id_bus="ENR-5837",
        student_id=student1.student_id,
        course_id=course1.course_id,
        status="CONFIRMED",
    )

    enrolment2 = Enrolment(
        enrolment_id_bus="ENR-5193",
        student_id=student1.student_id,
        course_id=course3.course_id,
        status="CONFIRMED",
    )

    enrolment3 = Enrolment(
        enrolment_id_bus="ENR-7421",
        student_id=student2.student_id,
        course_id=course1.course_id,
        status="CONFIRMED",
    )

    # Chloe has enrolled but payment has not yet been confirmed.
    enrolment4 = Enrolment(
        enrolment_id_bus="ENR-9351",
        student_id=student2.student_id,
        course_id=course2.course_id,
        status="PENDING",
    )

    enrolment5 = Enrolment(
        enrolment_id_bus="ENR-6274",
        student_id=student3.student_id,
        course_id=course2.course_id,
        status="CONFIRMED",
    )

    enrolment6 = Enrolment(
        enrolment_id_bus="ENR-6815",
        student_id=student3.student_id,
        course_id=course3.course_id,
        status="CONFIRMED",
    )

    enrolment7 = Enrolment(
        enrolment_id_bus="ENR-8642",
        student_id=student4.student_id,
        course_id=course1.course_id,
        status="CONFIRMED",
    )

    db.session.add_all([
        enrolment1,
        enrolment2,
        enrolment3,
        enrolment4,
        enrolment5,
        enrolment6,
        enrolment7,
    ])

    db.session.flush()

    # --------------------------------------------------
    # Attendance
    # --------------------------------------------------

    attendance_records = [
        Attendance(
            enrolment_id=enrolment1.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-15"),
            status="PRESENT",
        ),
        Attendance(
            enrolment_id=enrolment3.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-15"),
            status="PRESENT",
        ),
        Attendance(
            enrolment_id=enrolment7.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-15"),
            status="LATE",
        ),
        Attendance(
            enrolment_id=enrolment1.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-22"),
            status="PRESENT",
        ),
        Attendance(
            enrolment_id=enrolment3.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-22"),
            status="LATE",
        ),
        Attendance(
            enrolment_id=enrolment7.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-22"),
            status="PRESENT",
        ),
        Attendance(
            enrolment_id=enrolment1.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-29"),
            status="PRESENT",
        ),
        Attendance(
            enrolment_id=enrolment3.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-29"),
            status="PRESENT",
        ),
        Attendance(
            enrolment_id=enrolment7.enrolment_id,
            attendance_date=date.fromisoformat("2026-09-29"),
            status="ABSENT",
        ),
    ]

    db.session.add_all(attendance_records)

    # --------------------------------------------------
    # Grades
    # --------------------------------------------------

    grades = [
        Grade(
            enrolment_id=enrolment1.enrolment_id,
            assessment_name="Python Fundamentals Assessment",
            score=88.50,
            feedback="Very good understanding of Python fundamentals.",
            graded_date=date.fromisoformat("2026-10-02"),
        ),
        Grade(
            enrolment_id=enrolment3.enrolment_id,
            assessment_name="Python Fundamentals Assessment",
            score=82.00,
            feedback="Good understanding with consistent performance.",
            graded_date=date.fromisoformat("2026-10-02"),
        ),
        Grade(
            enrolment_id=enrolment7.enrolment_id,
            assessment_name="Python Fundamentals Assessment",
            score=91.00,
            feedback="Excellent understanding and application of key concepts.",
            graded_date=date.fromisoformat("2026-10-02"),
        ),
    ]

    db.session.add_all(grades)

    # --------------------------------------------------
    # Commit
    # --------------------------------------------------

    db.session.commit()

    print("BrightPath database seeded successfully.")


if __name__ == "__main__":
    with app.app_context():
        seed_database()