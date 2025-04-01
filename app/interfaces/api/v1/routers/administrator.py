from uuid import UUID
from dependency_injector.wiring import inject, Provide
from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from application.dto.base import PaginatedResult
from application.dto.user_dto import UserProfileDTO
from application.services.user_service import UserService
from config.container import Container
from domain.exceptions.base import NotFoundError
from interfaces.dependencies.auth import get_current_user
from interfaces.dependencies.permissions import admin_permission
from interfaces.filters.base import BasePaginationParams

router = APIRouter(
    dependencies=[Depends(get_current_user), Depends(admin_permission)]
)


@router.get("/users", response_model=PaginatedResult[UserProfileDTO])
@inject
async def get_users(
        params: BasePaginationParams = Depends(),
        user_service: UserService = Depends(Provide[Container.services.user_service])
):
    user = await user_service.get_list_users(params)
    return user


@router.get("/users/{uid}", response_model=UserProfileDTO)
@inject
async def get_user(
        uid: UUID,
        user_service: UserService = Depends(Provide[Container.services.user_service])
):
    try:
        user = await user_service.get_user(uid)
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/users/{uid}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
        uid: UUID,
        user_service: UserService = Depends(Provide[Container.services.user_service])
):
    try:
        await user_service.delete_user(uid)
        return None
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
