from application.dto.user_dto import UserDTO, UserCreateDTO
from domain.interfaces.yandex_auth_service import IYandexAuthService
from domain.repositories.user import IUserRepository


class YandexAuthUseCase:
    def __init__(self, yandex_auth_service: IYandexAuthService, user_repo: IUserRepository):
        self.yandex_auth_service = yandex_auth_service
        self.user_repo = user_repo

    async def execute(self, code: str) -> UserDTO:
        """
           Получение токена и информации о пользователе через сервис
        """

        token_data = await self.yandex_auth_service.get_token(code)
        user_info = await self.yandex_auth_service.get_user_info(token_data.access_token)
        user_dto = UserCreateDTO.model_validate(user_info)
        user, _ = await self.user_repo.get_or_create(user_dto.dict())
        return UserDTO.model_validate(user)
