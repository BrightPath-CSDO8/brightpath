from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator


class CourseStatusEnum(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    course_id_bus: str
    course_name: str
    course_fee: float
    description: str
    schedule: str
    start_date: date
    end_date: date
    capacity: int
    # classroom: str | None
    teacher_id_bus: str
    classroom_id: int
    status: CourseStatusEnum

    # @field_validator("classroom", mode="before")
    # @classmethod
    # def get_classroom_name(cls, value):
    #     if value is None:
    #         return None
    #     return value.room_name


class CourseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course_name: str
    course_fee: Decimal
    description: str
    schedule: str
    start_date: date
    end_date: date
    capacity: int
    classroom_id: int
    teacher_id_bus: str

    @model_validator(mode="after")
    def check_capacity(self):
        if self.capacity <= 0:
            raise ValueError("Class size must be greater than 0.")
        return self

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
    status: CourseStatusEnum | None = None
    teacher_id_bus: str | None = None

    @model_validator(mode="after")
    def check_capacity(self):
        if self.capacity is not None and self.capacity <= 0:
            raise ValueError("Class size must be greater than 0.")
        return self

    @model_validator(mode="after")
    def check_course_date(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date >= self.end_date
        ):
            raise ValueError("End date must be after start date.")
        return self
