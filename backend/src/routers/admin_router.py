from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_async_session
from src.models.settings import settings
from src.models.bookings import booking
from src.schemas.user_schema import UserSchema
from src.schemas.settings_schema import ChangeAutoconfirmSchema
from src.schemas.booking_schema import ResponseBookingSchema
from src.auth.utils.jwt_manager import get_current_superuser
from src.utils.booking_utils import get_headset_name, change_booking_status
from sqlalchemy import select, update


router = APIRouter()


@router.get(
    '/autoconfirm',
    status_code=status.HTTP_200_OK
)
async def get_autoconfirm(
    user: UserSchema = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(settings.c.auto_confirm)
    auto_confirm = (await session.execute(query)).fetchone()

    if not auto_confirm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Autoconfirm setting is not set')
    
    auto_confirm = auto_confirm[0]

    return {'autoconfrim': auto_confirm}


@router.post(
    '/autoconfirm',
    status_code=status.HTTP_204_NO_CONTENT
)
async def post_autoconfirm(
    autoconfirm_data: ChangeAutoconfirmSchema,
    user: UserSchema = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    query = select(settings.c.auto_confirm)
    auto_confirm = (await session.execute(query)).fetchone()

    if not auto_confirm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Autoconfirm setting is not set')
    
    auto_confirm = auto_confirm[0]

    if autoconfirm_data.autoconfirm == auto_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Autoconfirm setting is already {auto_confirm}')

    stmt = update(
        settings
    ).values(
        auto_confirm=autoconfirm_data.autoconfirm
    )

    await session.execute(stmt)
    await session.commit()

    return


@router.get(
    '/for_confirm',
    status_code=status.HTTP_200_OK
)
async def get_bookings_for_confirm(
    user: UserSchema = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(
        booking
    ).where(
        booking.c.status == 'pending'
    )

    bookings = (await session.execute(query)).fetchall()

    if not bookings:
        return {'result': []}

    result = [
        ResponseBookingSchema(
            booking_id=booking.id,
            headset_name=await get_headset_name(booking.headset_id, session),
            start_time=booking.start_time,
            end_time=booking.end_time,
            status=booking.status
        ) for booking in bookings
    ]
    
    return {"result": result}


@router.post(
    '/{booking_id}/confirm',
    status_code=status.HTTP_200_OK
)
async def get_bookings_for_confirm(
    booking_id: int, 
    user: UserSchema = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    return await change_booking_status(booking_id, session, user, 'confirmed')


@router.post(
    '/{booking_id}/cancel',
    status_code=status.HTTP_200_OK
)
async def get_bookings_for_confirm(
    booking_id: int, 
    user: UserSchema = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    return await change_booking_status(booking_id, session, user, 'cancelled')
