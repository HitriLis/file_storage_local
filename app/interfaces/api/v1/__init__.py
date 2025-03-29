from fastapi import APIRouter
from interfaces.api.v1.routers import auth_router
api_router = APIRouter()

# Регистрация маршрутов
api_router.include_router(auth_router, prefix="", tags=["Authentication"])

