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


## For internal use only
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    email: EmailStr
    role: UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    role: UserRole


#### STUDENT
class StudentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=5)
    first_name: str
    last_name: str
    mobile: str = Field(pattern=r"^[89]\d{7}$")
    dob: date

    @field_validator("email")
    @classmethod
    def validate_emaill(cls, value):
        if not value:
            raise ValueError("Email cannot be empty.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password cannot be empty.")
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long.")
        return value

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value):
        if not value.strip():
            raise ValueError("First Name cannot be empty.")
        return value

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        if not value.strip():
            raise ValueError("Last Name cannot be empty.")
        return value

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value):
        if value >= date.today():
            raise ValueError("Date of birth must be earlier than today.")
        return value


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
    mobile: str | None = Field(default=None, pattern=r"^[89]\d{7}$")


###### TEACHER
class TeacherCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=5)
    salutation: Salutation
    first_name: str
    last_name: str
    mobile: str = Field(pattern=r"^[89]\d{7}$")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password cannot be empty.")
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long.")
        return value

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value):
        if not value.strip():
            raise ValueError("First Name cannot be empty.")
        return value

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        if not value.strip():
            raise ValueError("Last Name cannot be empty.")
        return value


class TeacherRegistrationResponse(BaseModel):
    user: UserResponse
    teacher: TeacherProfile


class TeacherProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    teacher_id: int
    teacher_id_bus: str
    salutation: str
    first_name: str
    last_name: str
    mobile: str
    status: str


class TeacherProfileRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    salutation: str
    mobile: str | None = Field(default=None, pattern=r"^[89]\d{7}$")
    status: str


class LoginTeacherResponse(BaseModel):
    user: UserResponse
    teacher: TeacherProfile


###### ADMIN
class AdminCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=5)
    first_name: str
    last_name: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password cannot be empty.")
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long.")
        return value

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value):
        if not value.strip():
            raise ValueError("First Name cannot be empty.")
        return value

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        if not value.strip():
            raise ValueError("Last Name cannot be empty.")
        return value


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
