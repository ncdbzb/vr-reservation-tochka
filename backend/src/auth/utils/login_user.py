import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import user as db_user
from src.auth.utils.password_manager import verify_password
from config.config import SECRET_JWT, JWT_ALGORITHM, COOKIE_LIFETIME, JWT_TOKEN_LIFETIME


async def login_user(cred_data: dict, session: AsyncSession):
    query = select(db_user).where(db_user.c.email == cred_data['email'])
    user = (await session.execute(query)).fetchone()

    if not user or not user.is_active or not await verify_password(cred_data['password'], user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid credintials')
    

    response = Response(status_code=status.HTTP_204_NO_CONTENT)

    data = {"sub": str(user.id)}
    print(user.id)
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_TOKEN_LIFETIME)
    payload["exp"] = expire
    token = jwt.encode(payload, SECRET_JWT, algorithm=JWT_ALGORITHM)

    
    response.set_cookie(
        'vr_headset_booking',
        token,
        max_age=COOKIE_LIFETIME,
        secure=False,
        httponly=False,
        samesite="lax"
    )

    return response
