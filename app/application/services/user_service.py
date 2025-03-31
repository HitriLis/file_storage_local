from uuid import UUID
from application.dto.user_dto import UserProfileDTO, UserUpdateDTO
from domain.exceptions.base import NotFoundError, BadRequestError
from domain.repositories.user import IUserRepository

class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    async def delete_user(self, uid: UUID):
        user = await self._user_repo.delete_user(uid)
        if not user:
            raise NotFoundError("User does not")
        return user

    async def get_user(self, uid: UUID):
        user = await self._user_repo.get_by_uid(uid)
        if not user:
            raise NotFoundError("User does not")
        return user

    async def get_profile(self, uid: UUID) -> UserProfileDTO:
        user = await self._user_repo.get_by_uid(uid)
        return UserProfileDTO.model_validate(user)

    async def update_profile(self, uid: UUID, data: UserUpdateDTO) -> UserProfileDTO:
        if data.username:
            exist_username = await self._user_repo.exist_username(data.username)
            if exist_username:
                raise BadRequestError("Username already exists")
        update_data = data.model_dump(exclude_none=True)
        user = await self._user_repo.update_user(uid, update_data)
        return UserProfileDTO.model_validate(user)
