from uuid import UUID
from fastapi import UploadFile

from application.dto.files import FileDTO
from domain.exceptions.base import BadRequestError, NotFoundError
from application.services.upload_file import UploadFileService
from domain.repositories.files import IFilesRepository


class UploadFileUseCase:
    def __init__(self, file_repo: IFilesRepository, upload_service: UploadFileService):
        self._file_repo = file_repo
        self._upload_service = upload_service

    async def execute(self, user_id: UUID, file: UploadFile, filename: str = None) -> FileDTO:
        try:
            file = await self._upload_service.upload(str(user_id), file, filename)
            file_data = await self._file_repo.create_file({
                "user_id": user_id,
                "filename": file.original_name,
                "path": file.path
            })
            return FileDTO.model_validate(file_data)
        except Exception as e:
            raise BadRequestError(str(e))


class DeleteFileUseCase:
    def __init__(self, file_repo: IFilesRepository, upload_service: UploadFileService):
        self._file_repo = file_repo
        self._upload_service = upload_service

    async def execute(self, user_id: UUID, uid: UUID) -> None:
        try:
            file = await self._file_repo.get_by_uid(user_id, uid)
            if not file:
                raise NotFoundError("File does not")
            await self._upload_service.delete_file(str(user_id), file.path)
            await self._file_repo.delete_file(user_id, uid)
        except Exception as e:
            raise BadRequestError(str(e))
