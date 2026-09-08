from app import app
from extensions import db
from models import Users, Student, Teacher, Admin, Classroom, Course, Enrolment, Attendance, Grade
from datetime import date

with app.app_context():

    # Create test users
    student_user = Users(
        entra_object_id=None,
        email="student@test.com",
        role="STUDENT"
    )

    teacher_user = Users(
        entra_object_id=None,
        email="teacher@test.com",
        role="TEACHER"
    )

    admin_user = Users(
        entra_object_id=None,
        email="admin@test.com",
        role="ADMIN"
    )

    db.session.add_all([
        student_user,
        teacher_user,
        admin_user
    ])

    db.session.commit()

    print("Test users created successfully.")

    # Create Student profile
    student = Student(
        student_id_bus="STU-0001",
        user_id=student_user.user_id,
        first_name="Test",
        last_name="Student",
        dob=date(2005, 9, 15),
        mobile="91234567",
        status="ACTIVE"
    )

    # Create Teacher profile
    teacher = Teacher(
        teacher_id_bus="TCH-0001",
        user_id=teacher_user.user_id,
        salutation="Mr",
        first_name="Test",
        last_name="Teacher",
        mobile="92345678",
        status="ACTIVE"
    )

    # Create Admin profile
    admin = Admin(
        user_id=admin_user.user_id,
        first_name="Test",
        last_name="Admin"
    )

    db.session.add_all([
        student,
        teacher,
        admin
    ])

    db.session.commit()

    print("Student, Teacher and Admin created successfully.")

    # Create Classroom
    classroom = Classroom(
        room_name="Room A",
        class_capacity=30
    )

    db.session.add(classroom)
    db.session.commit()

    print("Classroom created successfully.")

    # Create Course
    course = Course(
        course_id_bus="CSR-0001",
        course_name="Introduction to Python",
        description="Basic Python course",
        course_fee=200.00,
        schedule="Monday 10:00-12:00",
        start_date=date(2026, 9, 10),
        end_date=date(2026, 10, 10),
        status="PENDING",
        capacity=20,
        teacher_id=teacher.teacher_id,
        classroom_id=classroom.classroom_id
    )

    db.session.add(course)
    db.session.commit()

    print("Course created successfully.")

    # Create Enrolment
    enrolment = Enrolment(
        enrolment_id_bus="ENR-0001",
        student_id=student.student_id,
        course_id=course.course_id,
        status="PENDING"
    )

    db.session.add(enrolment)
    db.session.commit()

    print("Enrolment created successfully.")

    # Create Attendance
    attendance = Attendance(
        enrolment_id=enrolment.enrolment_id,
        attendance_date=date(2026, 9, 15),
        status="PRESENT"
    )

    # Create Grade
    grade = Grade(
        enrolment_id=enrolment.enrolment_id,
        assessment_name="Quiz 1",
        score=85.00,
        feedback="Good work",
        graded_date=date(2026, 9, 20)
    )

    db.session.add_all([
        attendance,
        grade
    ])

    db.session.commit()

    print("Attendance and Grade created successfully.")

    # Test duplicate enrolment
    try:
        duplicate_enrolment = Enrolment(
            enrolment_id_bus="ENR-0002",
            student_id=student.student_id,
            course_id=course.course_id,
            status="PENDING"
        )

        db.session.add(duplicate_enrolment)
        db.session.commit()

        print("ERROR: Duplicate enrolment was allowed.")

    except Exception:
        db.session.rollback()
        print("PASS: Duplicate enrolment was blocked.")


    # Test duplicate attendance
    try:
        duplicate_attendance = Attendance(
            enrolment_id=enrolment.enrolment_id,
            attendance_date=date(2026, 9, 15),
            status="ABSENT"
        )

        db.session.add(duplicate_attendance)
        db.session.commit()

        print("ERROR: Duplicate attendance was allowed.")

    except Exception:
        db.session.rollback()
        print("PASS: Duplicate attendance was blocked.")

        # Test duplicate Student user_id
    try:
        duplicate_student = Student(
            student_id_bus="STU-0002",
            user_id=student_user.user_id,
            first_name="Another",
            last_name="Student",
            dob=date(2006, 1, 1),
            mobile="93456789",
            status="ACTIVE"
        )

        db.session.add(duplicate_student)
        db.session.commit()

        print("ERROR: Duplicate Student user_id was allowed.")

    except Exception:
        db.session.rollback()
        print("PASS: Duplicate Student user_id was blocked.")

        # Test duplicate Teacher user_id
    try:
        duplicate_teacher = Teacher(
            teacher_id_bus="TCH-0002",
            user_id=teacher_user.user_id,
            salutation="Ms",
            first_name="Another",
            last_name="Teacher",
            mobile="94567890",
            status="ACTIVE"
        )

        db.session.add(duplicate_teacher)
        db.session.commit()

        print("ERROR: Duplicate Teacher user_id was allowed.")

    except Exception:
        db.session.rollback()
        print("PASS: Duplicate Teacher user_id was blocked.")

    # Test duplicate Admin user_id
    try:
        duplicate_admin = Admin(
            user_id=admin_user.user_id,
            first_name="Another",
            last_name="Admin"
        )

        db.session.add(duplicate_admin)
        db.session.commit()

        print("ERROR: Duplicate Admin user_id was allowed.")

    except Exception:
        db.session.rollback()
        print("PASS: Duplicate Admin user_id was blocked.")