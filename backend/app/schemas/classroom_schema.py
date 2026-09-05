from pydantic import BaseModel, ConfigDict


class ClassroomCreate(BaseModel):
    room_name: str
    class_capacity: int


class AllClassrooms(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    room_name: str
    class_capacity: int
