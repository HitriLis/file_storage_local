from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.container import Container
from application.services.auth_service import AuthTokenService
from domain.models.users import User
from domain.repositories.user import IUserRepository
security = HTTPBearer()


@inject
async def get_current_user(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        auth_service: AuthTokenService = Depends(Provide[Container.services.auth_service]),
        user_repo: IUserRepository = Depends(Provide[Container.repository.user_repo])

) -> Request:
    token = credentials.credentials
    try:
        payload = auth_service.decode_token(token)
        uid = payload.pop('sub')
        user: User = await user_repo.get_by_uid(uid)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        request.state.user = user
        return request
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
