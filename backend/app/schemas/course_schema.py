from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator


class CourseStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    course_id_bus: str
    course_name: str
    course_fee: Decimal
    description: str
    schedule: str
    start_date: date
    end_date: date
    capacity: int
    classroom: str | None
    status: CourseStatus

    @field_validator("classroom", mode="before")
    @classmethod
    def get_classroom_name(cls, value):
        if value is None:
            return None
        return value.room_name


class CourseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course_name: str
    course_fee: Decimal
    description: str
    schedule: str
    start_date: date
    end_date: date
    capacity: int
    classroom_id: int | None = None

    @model_validator(mode="after")
    def check_course_date(self):
        if self.start_date >= self.end_date:
            raise ValueError("End date must be on or after start date")
        return self


# fields are None because its a PATCH schema
# None default means this field is optional in a PATCH
class CoursePatchRequest(BaseModel):
    # Disallow unknown fields from request
    model_config = ConfigDict(extra="forbid")

    course_name: str | None = None
    course_fee: Decimal | None = None
    description: str | None = None
    schedule: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    capacity: int | None = None
    classroom_id: int | None = None
    status: CourseStatus | None = None
