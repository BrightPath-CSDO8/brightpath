from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class CourseStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


class CoursePostRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course_name: str
    course_fee: Decimal
    description: str
    schedule: str
    start_date: date
    end_date: date
    capacity: int


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
    status: CourseStatus | None = None
