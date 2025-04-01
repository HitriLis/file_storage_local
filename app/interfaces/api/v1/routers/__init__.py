from .auth import router as auth_router
from .user import router as user_router
from .administrator import router as admin_router
from .file import router as file_router

__all__ = [
    "auth_router",
    "user_router",
    "admin_router",
    "file_router"
]
