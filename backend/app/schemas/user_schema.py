from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class UserRole(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    role: UserRole


#### STUDENT


class StudentCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    mobile: str = Field(pattern=r"^[89]\d{7}$")
    dob: date


class StudentProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id_bus: str
    first_name: str
    last_name: str
    status: str
    mobile: str | None = None
    dob: date | None = None


class StudentRegistrationResponse(BaseModel):
    user: UserResponse
    student: StudentProfile


class LoginStudentResponse(BaseModel):
    user: UserResponse
    student: StudentProfile


###### TEACHER


class TeacherRegistrationResponse(BaseModel):
    user: UserResponse


class TeacherProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    teacher_id_bus: str
    salutation: str
    first_name: str
    last_name: str
    mobile: str
    status: str


class LoginTeacherResponse(BaseModel):
    user: UserResponse
    teacher: TeacherProfile


###### ADMIN
class AdminProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str


class LoginAdminResponse(BaseModel):
    user: UserResponse
    admin: AdminProfile


###### SUPERADMIN
#
