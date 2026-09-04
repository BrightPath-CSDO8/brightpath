from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class UserRole(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class StudentCreate(BaseModel):
    # email: EmailStr
    # password: str
    first_name: str
    last_name: str
    mobile: str = Field(pattern=r"^[89]\d{7}$")
    dob: date


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id_bus: str
    first_name: str
    last_name: str
    mobile: str
    dob: date
    role: UserRole


class StaffCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
