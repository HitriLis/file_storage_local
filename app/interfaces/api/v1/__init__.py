from fastapi import APIRouter
from interfaces.api.v1.routers import auth_router
from interfaces.api.v1.routers import user_router
from interfaces.api.v1.routers import admin_router
from interfaces.api.v1.routers import file_router
api_router = APIRouter()

# Регистрация маршрутов
api_router.include_router(auth_router, prefix="", tags=["Authentication"])
api_router.include_router(user_router, prefix="", tags=["User"])
api_router.include_router(file_router, prefix="", tags=["File"])
api_router.include_router(admin_router, prefix="", tags=["Admin"])


