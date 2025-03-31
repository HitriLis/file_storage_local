from pydantic import BaseModel


class UserDTO(BaseModel):
    uid: str
    email: str
