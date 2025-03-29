from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/login")
@inject
async def login() -> JSONResponse:
    pass
