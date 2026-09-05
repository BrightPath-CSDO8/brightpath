from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EnrollmentCreate(BaseModel):
    course_id_bus: str
