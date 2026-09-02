from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class StudentCreate(BaseModel):
    email: EmailStr
    password: str


class StaffCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
