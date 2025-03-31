from pydantic import BaseModel


class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenRefreshResponseDTO(BaseModel):
    access_token: str
    token_type: str = "Bearer"
