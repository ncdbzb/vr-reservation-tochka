from fastapi import HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import user
from src.auth.utils.password_manager import get_hashed_password, validate_password


async def create_user(user_dict: dict, session: AsyncSession):
    password = user_dict.pop('password')

    if not await validate_password(password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password must be at least 6 characters long")
    
    query = select(user).where(user.c.email == user_dict['email'])
    result = await session.execute(query)

    if result.fetchone():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email alredy exists")
    
    hashed_password = await get_hashed_password(password)

    try:
        stmt = insert(user).values(email=user_dict['email'], hashed_password=str(hashed_password), is_active=True, is_superuser=False)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'Successful registration!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)