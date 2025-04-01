from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, field_serializer


class FileDTO(BaseModel):
    uid: UUID
    filename: str
    path: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @field_serializer("uid")
    def serialize_uid(self, value: UUID, _info):
        return str(value)

    @field_serializer("created_at")
    def serialize_created_at(self, dt: datetime, _info):
        return dt.strftime("%d-%m-%Y")

    @field_serializer("updated_at")
    def serialize_updated_at(self, dt: datetime, _info):
        return dt.strftime("%d-%m-%Y")

    class Config:
        from_attributes = True


class FileCreateDTO(BaseModel):
    filename: str
    path: str
    original_name: str
