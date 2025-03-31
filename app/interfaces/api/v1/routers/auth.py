from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from application.dto.token_dto import TokenResponseDTO, TokenRefreshResponseDTO
from application.services.auth_service import AuthTokenService
from application.use_cases.yandex_auth import YandexAuthUseCase
from config.container import Container
from domain.exceptions.auth_exceptions import InvalidCredentialsException
from infrastructure.services.yandex_auth_service import YandexAuthService

router = APIRouter()


@router.get("/yandex/login")
@inject
async def yandex_login(
        yandex_auth_service: YandexAuthService = Depends(Provide[Container.services.yandex_auth_service]),
):
    yandex_auth_url = yandex_auth_service.get_auth_url
    return {"authorize_url": yandex_auth_url}


# TokenResponseDTO

@router.get(
    "/yandex/callback",
    summary="Yandex OAuth callback",
    description="Exchanges Yandex authorization code for a JWT token.",
    responses={
        200: {"description": "JWT token returned successfully"},
        401: {"description": "Invalid authorization code"}
    },
    response_model=TokenResponseDTO
)
@inject
async def yandex_callback(
        code: str,
        use_case: YandexAuthUseCase = Depends(Provide[Container.use_cases.yandex_auth_use_case]),
        auth_service: AuthTokenService = Depends(Provide[Container.services.auth_service]),
):
    try:
        user_dto = await use_case.execute(code)
        tokens = auth_service.create_tokens(user_dto)
        return tokens
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenRefreshResponseDTO)
@inject
async def get_refresh_token(
     auth_service: AuthTokenService = Depends(Provide[Container.services.auth_service]),
):
    # Проверяем refresh token
    try:
        data = await auth_service.refresh_token('data.refresh_token')
        if not data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return data
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
