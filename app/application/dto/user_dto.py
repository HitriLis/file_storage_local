from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, field_serializer


class UserDTO(BaseModel):
    uid: UUID
    email: str
    username: Optional[str] = None

    @field_serializer("uid")
    def serialize_uid(self, value: UUID, _info):
        return str(value)

    class Config:
        from_attributes = True


class UserProfileDTO(UserDTO):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateDTO(BaseModel):
    email: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
