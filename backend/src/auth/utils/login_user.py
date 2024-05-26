from fastapi import HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import user


async def login_user(cred_data: dict, session: AsyncSession):
    query = select(user).where(user.c.email == cred_data['email'])