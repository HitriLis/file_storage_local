from uuid import UUID

from application.dto.base import PaginatedResult
from application.dto.user_dto import UserProfileDTO, UserUpdateDTO
from domain.exceptions.base import NotFoundError, BadRequestError
from domain.repositories.user import IUserRepository
from interfaces.filters.base import BasePaginationParams


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    async def get_list_users(self, params: BasePaginationParams) -> PaginatedResult:
        offset = self._get_pagination_offset(params.page, params.page_size)
        total, users = await self._user_repo.users_list(offset, params.page_size)
        return PaginatedResult.create(data=users, total=total, page=params.page, page_size=params.page_size)

    async def delete_user(self, uid: UUID) -> None:
        user = await self._user_repo.exist_user(uid)
        if not user:
            raise NotFoundError("User does not")
        await self._user_repo.delete_user(uid)

    async def get_user(self, uid: UUID) -> UserProfileDTO:
        user = await self._user_repo.get_by_uid(uid)
        if not user:
            raise NotFoundError("User does not")
        return UserProfileDTO.from_orm(user)

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

    @staticmethod
    def _get_pagination_offset(page: int, page_size: int) -> int:
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        return offset
