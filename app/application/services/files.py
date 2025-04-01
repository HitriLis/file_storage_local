from uuid import UUID
from typing import Optional
from application.dto.base import PaginatedResult
from application.dto.files import FileDTO, FileCreateDTO
from domain.exceptions.base import NotFoundError, BadRequestError
from domain.repositories.files import IFilesRepository
from interfaces.filters.base import BasePaginationParams


class FileService:
    def __init__(self, file_repo: IFilesRepository):
        self._file_repo = file_repo

    async def get_files(self, user_id: UUID, params: BasePaginationParams) -> PaginatedResult:
        offset = self._get_pagination_offset(params.page, params.page_size)
        total, users = await self._file_repo.file_list(user_id, offset, params.page_size)
        return PaginatedResult.create(data=users, total=total, page=params.page, page_size=params.page_size)

    async def get_file(self, user_id: UUID, uid: UUID) -> Optional[FileDTO]:
        file = await self._file_repo.get_by_uid(user_id, uid)
        if not file:
            raise NotFoundError("File does not")
        return FileDTO.model_validate(file)

    @staticmethod
    def _get_pagination_offset(page: int, page_size: int) -> int:
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        return offset
