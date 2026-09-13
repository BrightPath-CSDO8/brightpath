from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator

# Schema
from backend.app.schemas.course_schema import CourseStatusEnum


class TeacherCourse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    course_id_bus: str
    course_name: str
    description: str
    schedule: str
    start_date: date
    end_date: date
    capacity: int
    classroom_id: int
    status: CourseStatusEnum


class CourseStudents(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id_bus: str
    first_name: str
    last_name: str
    mobile: str
    enrolment_id_bus: str


class AttendanceStatusEnum(str, Enum):
    PRESENT = "PRESENT"
    LATE = "LATE"
    ABSENT = "ABSENT"


class AttendanceStudent(BaseModel):
    enrolment_id_bus: str
    status: AttendanceStatusEnum


class BulkAttendanceUpdate(BaseModel):
    attendance_date: date
    students: list[AttendanceStudent]
