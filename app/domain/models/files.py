from datetime import datetime
from uuid import UUID
from dataclasses import dataclass


@dataclass
class File:
    uid: UUID
    filename: str
    path: str
    created_at: datetime = None
    updated_at: datetime = None
