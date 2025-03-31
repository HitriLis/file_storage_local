from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    uid: UUID
    is_admin: bool
    username: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
