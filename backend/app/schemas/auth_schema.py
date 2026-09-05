from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


# Schema for Entra ID Authentication
class AuthenticatedIdentity(BaseModel):
    entra_object_id: str
    email: EmailStr


# Old login schema (Temporary)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
