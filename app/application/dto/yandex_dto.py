from typing import Optional
from pydantic import BaseModel


class YandexUserResponseDTO(BaseModel):
    email: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    number: Optional[str] = None


class YandexTokenDTO(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
