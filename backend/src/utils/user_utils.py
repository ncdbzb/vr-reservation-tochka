from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.users import user as User
from src.schemas.user_schema import UserUpdateSchema

async def update_user(session: AsyncSession, user_id: int, user_update: UserUpdateSchema):
    query = select(User).where(User.c.id == user_id)
    result = await session.execute(query)
    existing_user = result.fetchone()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    stmt = (
        update(User)
        .where(User.c.id == user_id)
        .values(**update_data)
        .returning(User)
    )
    result = await session.execute(stmt)
    await session.commit()

    updated_user = result.fetchone()
    return dict(updated_user._mapping)


async def delete_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.c.id == user_id)
    result = await session.execute(query)
    user = result.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    stmt = delete(User).where(User.c.id == user_id)
    await session.execute(stmt)
    await session.commit()
