from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)
    confirm_password: str = Field(min_length=5)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value):
        if not value.strip():
            raise ValueError("Password cannot be empty.")
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long.")
        return value


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_password: str = Field(min_length=5)
    new_email: EmailStr
