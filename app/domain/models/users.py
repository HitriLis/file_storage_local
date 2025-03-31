from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    uid: UUID
    username: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
