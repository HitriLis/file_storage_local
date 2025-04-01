from dependency_injector.wiring import inject, Provide
from starlette import status
from fastapi import APIRouter, Request, Depends, HTTPException

from application.dto.user_dto import UserProfileDTO, UserUpdateDTO
from application.services.user_service import UserService
from config.container import Container
from domain.exceptions.base import BadRequestError
from interfaces.dependencies.auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/profile", response_model=UserProfileDTO)
@inject
async def profile(
        request: Request,
        user_service: UserService = Depends(Provide[Container.services.user_service])
):
    user = request.state.user
    profile_user = await user_service.get_profile(user.uid)
    return profile_user


@router.put("/profile", response_model=UserProfileDTO)
@inject
async def update_profile(
        request: Request,
        data: UserUpdateDTO,
        user_service: UserService = Depends(Provide[Container.services.user_service])
):
    user = request.state.user
    try:
        profile_user = await user_service.update_profile(user.uid, data)
        return profile_user
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


