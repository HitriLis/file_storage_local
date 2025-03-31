from datetime import datetime, timedelta
import jwt

from application.dto.token_dto import TokenResponseDTO, TokenRefreshResponseDTO
from application.dto.user_dto import UserDTO
from domain.exceptions.auth_exceptions import InvalidCredentialsException


class AuthTokenService:
    def __init__(self,
                 secret_key: str,
                 algorithm: str,
                 access_token_expire_minutes: int,
                 refresh_token_expire_days: int
                 ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def _create_access_token(self, payload: dict) -> str:
        """Создает access token."""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def _create_refresh_token(self, payload: dict) -> str:
        """Создает refresh token."""

        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def _decode_token(self, token: str) -> dict:
        try:

            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            sub = payload.get("sub")
            if not sub:
                raise InvalidCredentialsException("No subject found in refresh token")
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidCredentialsException("Token expired")
        except jwt.InvalidTokenError:
            raise InvalidCredentialsException("Invalid token")

    def create_tokens(self, data: UserDTO) -> TokenResponseDTO:
        """
        Создает JWT refresh-токен с длительным сроком действия.
        """
        try:
            data = {"sub": data.uid}
            access_token = self._create_access_token(data)
            # Опционально: создаем новый refresh-токен для ротации
            refresh_token = self._create_refresh_token(data)
            return TokenResponseDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer"
            )
        except Exception as e:
            raise InvalidCredentialsException(f"Error creating refresh token: {str(e)}")

    #
    def refresh_token(self, refresh_token: str) -> TokenRefreshResponseDTO:
        """
        Обновляет access-токен на основе refresh-токена.
        """

        payload = self._decode_token(refresh_token)
        sub = payload.get("sub")
        # Создаем новый access-токен
        new_access_token = self._create_access_token(data={"sub": sub})
        return TokenRefreshResponseDTO(
            access_token=new_access_token,
            token_type="Bearer"
        )
