from uuid import UUID
from dependency_injector.wiring import inject, Provide
from starlette import status
from fastapi import APIRouter, Request, UploadFile, File, Depends, Form, HTTPException

from application.dto.base import PaginatedResult
from application.dto.files import FileDTO
from application.services.files import FileService
from application.use_cases.upload_file import UploadFileUseCase, DeleteFileUseCase
from config.container import Container
from domain.exceptions.base import BadRequestError, NotFoundError
from interfaces.dependencies.auth import get_current_user
from interfaces.filters.base import BasePaginationParams

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/files")
@inject
async def create_file(
        request: Request,
        use_case: UploadFileUseCase = Depends(Provide[Container.use_cases.upload_file]),
        file: UploadFile = File(...),
        filename: str = Form(None)
):
    try:
        user = request.state.user
        files = await use_case.execute(user.uid, file, filename)
        return files
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/files", response_model=PaginatedResult[FileDTO])
@inject
async def get_files_list(
        request: Request,
        params: BasePaginationParams = Depends(),
        file_service: FileService = Depends(Provide[Container.services.file_service])
):
    user = request.state.user
    files = await file_service.get_files(user.uid, params)
    return files


@router.get("/files/{uid}", response_model=FileDTO)
@inject
async def get_file(
        request: Request,
        uid: UUID,
        file_service: FileService = Depends(Provide[Container.services.file_service])
):
    try:
        user = request.state.user
        files = await file_service.get_file(user.uid, uid)
        return files
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/files/{uid}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_file(
        request: Request,
        uid: UUID,
        use_case: DeleteFileUseCase = Depends(Provide[Container.use_cases.delete_file])
):

    try:
        user = request.state.user
        await use_case.execute(user.uid, uid)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
