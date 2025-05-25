from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_async_session
from src.schemas.user_schema import UserSchema, UserUpdateSchema
from src.auth.utils.jwt_manager import get_current_user
from src.utils.user_utils import update_user, delete_user


router = APIRouter()

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema
)
async def get_me(
    user: UserSchema = Depends(get_current_user)
):
    return user


@router.patch(
    "/me",
    response_model=UserSchema,
)
async def update_user_me(
    user_update: UserUpdateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: UserSchema = Depends(get_current_user)
):
    return await update_user(session, user.id, user_update)


@router.delete("/me", status_code=204)
async def delete_user_me(
    session: AsyncSession = Depends(get_async_session),
    user: UserSchema = Depends(get_current_user)
):
    await delete_user(session, user.id)
    return
