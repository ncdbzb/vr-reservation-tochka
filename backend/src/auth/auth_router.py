from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schema import UserSchema, UserLogin
from src.auth.utils.create_user import create_user
from src.auth.utils.login_user import login_user
from config.database import get_async_session


router = APIRouter()

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_create: UserSchema,
    session: AsyncSession = Depends(get_async_session)
):
    return await create_user(user_create.dict(), session)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    return await login_user(user_login.dict(), session)