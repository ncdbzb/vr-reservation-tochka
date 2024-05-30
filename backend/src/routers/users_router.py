from fastapi import APIRouter, status, Depends

from src.schemas.user_schema import UserSchema
from src.auth.utils.jwt_manager import get_current_user


router = APIRouter()

@router.get(
    "/me",
    status_code=status.HTTP_200_OK
)
async def get_me(
    user: UserSchema = Depends(get_current_user)
):
    return user
