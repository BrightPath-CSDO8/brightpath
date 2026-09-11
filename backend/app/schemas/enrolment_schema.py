from enum import Enum
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from backend.app.schemas.user_schema import StudentProfile


class EnrolmentEnum(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"


class AdminAllEnrolments(BaseModel):
    enrolment_id_bus: str
    course_id_bus: str
    course_name: str
    student_id_bus: str
    first_name: str
    last_name: str
    status: EnrolmentEnum


class EnrolmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course_id_bus: str


class EnrolmentCreateResponse(BaseModel):
    # student: StudentProfile
    enrolment_id_bus: str
    status: str


class StudentAllEnrolments(BaseModel):
    enrolment_id_bus: str
    course_id_bus: str
    course_name: str
    start_date: date
    end_date: date
    enrolment_date: datetime
    status: EnrolmentEnum


class AdminUpdateEnrolment(BaseModel):
    status: EnrolmentEnum
