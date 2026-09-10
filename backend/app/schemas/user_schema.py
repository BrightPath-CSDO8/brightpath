from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class UserRole(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class Salutation(str, Enum):
    MR = "Mr"
    MRS = "Mrs"
    MS = "Ms"
    PROF = "Prof"
    DR = "Dr"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    role: UserRole


#### STUDENT
class StudentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
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


# fields are None because its a PATCH schema
# None default means this field is optional in a PATCH
class StudentProfileRequest(BaseModel):
    # Disallow unknown fields from request
    model_config = ConfigDict(extra="forbid")
    mobile: str | None = None


###### TEACHER
class TeacherCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str
    salutation: Salutation
    first_name: str
    last_name: str
    mobile: str


class TeacherRegistrationResponse(BaseModel):
    user: UserResponse
    teacher: TeacherProfile


class TeacherProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    teacher_id_bus: str
    salutation: str
    first_name: str
    last_name: str
    mobile: str
    status: str


class TeacherProfileRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    salutation: str
    mobile: str
    status: str


class LoginTeacherResponse(BaseModel):
    user: UserResponse
    teacher: TeacherProfile


###### ADMIN
class AdminCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class AdminCreateResponse(BaseModel):
    user: UserResponse
    admin: AdminProfile


class AdminProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str


class LoginAdminResponse(BaseModel):
    user: UserResponse
    admin: AdminProfile


###### SUPERADMIN
#
