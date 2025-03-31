from fastapi import HTTPException, Request
from domain.models.users import User


async def admin_permission(request: Request):
    user: User = getattr(request.state, "user", None)

    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
