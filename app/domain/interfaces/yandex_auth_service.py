from abc import ABC, abstractmethod
from application.dto.yandex_dto import YandexTokenDTO, YandexUserResponseDTO


class IYandexAuthService(ABC):

    @property
    @abstractmethod
    def get_auth_url(self) -> str:
        pass

    @abstractmethod
    async def get_token(self, code: str) -> YandexTokenDTO:
        pass

    @staticmethod
    @abstractmethod
    async def get_user_info(access_token: str) -> YandexUserResponseDTO:
        pass
