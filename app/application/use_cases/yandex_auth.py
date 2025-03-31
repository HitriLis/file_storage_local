from application.dto.user_dto import UserDTO
from domain.interfaces.yandex_auth_service import IYandexAuthService


class YandexAuthUseCase:
    def __init__(self, yandex_auth_service: IYandexAuthService):
        self.yandex_auth_service = yandex_auth_service

    async def execute(self, code: str) -> UserDTO:
        # Получение токена и информации о пользователе через сервис

        token_data = await self.yandex_auth_service.get_token(code)
        user_info = await self.yandex_auth_service.get_user_info(token_data.access_token)
        return UserDTO(email=user_info.email, uid='uid')
