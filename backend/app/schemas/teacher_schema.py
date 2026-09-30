from enum import Enum
from datetime import date
from decimal import Decimal
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

    @field_validator("attendance_date")
    @classmethod
    def validate_attendance_date(cls, value):
        if value > date.today():
            raise ValueError("Attendance date must be ealier than or today.")
        return value


class GradeStudent(BaseModel):
    enrolment_id_bus: str
    score: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    feedback: str | None = None


class BulkGradesUpdate(BaseModel):
    graded_date: date
    assessment_name: str
    students: list[GradeStudent]

    @field_validator("graded_date")
    @classmethod
    def validate_graded_date(cls, value):
        if value > date.today():
            raise ValueError("Assessment date must only be earlier than or today.")
        return value
