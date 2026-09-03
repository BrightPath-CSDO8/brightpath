from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
