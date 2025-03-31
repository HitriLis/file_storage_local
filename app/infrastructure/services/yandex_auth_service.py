import httpx

from application.dto.yandex_dto import YandexTokenDTO, YandexUserResponseDTO
from domain.exceptions.auth_exceptions import InvalidCredentialsException
from domain.interfaces.yandex_auth_service import IYandexAuthService


class YandexAuthService(IYandexAuthService):

    def __init__(self, client_id: int, client_secret: int, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @property
    def get_auth_url(self) -> str:
        return (
            f"https://oauth.yandex.ru/authorize?"
            f"response_type=code&"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}"
        )

    async def get_token(self, code: str) -> YandexTokenDTO:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth.yandex.ru/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )

            if response.status_code != 200:
                raise InvalidCredentialsException("Failed to get Yandex token")
            return YandexTokenDTO(**response.json())

    @staticmethod
    async def get_user_info(access_token: str) -> YandexUserResponseDTO:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://login.yandex.ru/info",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code != 200:
                raise InvalidCredentialsException("Failed to get Yandex user info")
            data = response.json()
            email = data.get('default_email')
            login = data.get('login')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            number = data.get('number')
            return YandexUserResponseDTO(
                email=email,
                username=login,
                first_name=first_name,
                last_name=last_name,
                number=number
            )
