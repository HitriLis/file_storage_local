from fastapi import APIRouter
from interfaces.api.v1.routers import auth_router
from interfaces.api.v1.routers import user_router
api_router = APIRouter()

# Регистрация маршрутов
api_router.include_router(auth_router, prefix="", tags=["Authentication"])
api_router.include_router(user_router, prefix="", tags=["User"])

