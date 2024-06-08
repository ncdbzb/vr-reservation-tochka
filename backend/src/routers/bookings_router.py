from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_async_session
from src.models.bookings import booking
from src.models.settings import settings
from src.schemas.booking_schema import BookingTimeSchema, BookingCreateSchema, ResponseBookingSchema
from src.schemas.user_schema import UserSchema
from src.auth.utils.jwt_manager import get_current_user
from src.utils.convert_time import convert_time
from src.utils.booking_utils import get_headset_name, change_booking_status
from sqlalchemy import select, insert, and_


router = APIRouter()


@router.get(
    "/my",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def get_my_bookings(
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    query = select(
        booking
    ).where(
        booking.c.user_id == user.id
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
    '/{booking_id}/cancel_my',
    status_code=status.HTTP_204_NO_CONTENT
)
async def cancel_my(
    booking_id: int,
    user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    return await change_booking_status(booking_id, session, user, 'cancelled')


@router.get(
    "/{headset_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def get_bookings(
    headset_id: int, 
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    
    query = select(
        booking.c.start_time, 
        booking.c.end_time
    ).where(
        and_(
            booking.c.headset_id == headset_id,
            booking.c.status.in_(['confirmed', 'pending'])
        )    
    )
    
    bookings = (await session.execute(query)).fetchall()
    
    if not bookings:
        return {"result": []}
    
    result = [BookingTimeSchema.from_orm(booking) for booking in bookings]
    return {"result": result}


@router.post(
    '/book',
    status_code=status.HTTP_201_CREATED
)
async def book(
    booking_request: BookingCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: UserSchema = Depends(get_current_user)
) -> dict:
    
    query = select(
        booking
    ).where(
        and_(      
            booking.c.headset_id == booking_request.headset_id,
            booking.c.status.in_(['confirmed', 'pending']),
            booking.c.start_time == convert_time(booking_request.start_time),
            booking.c.end_time == convert_time(booking_request.end_time)
        )
    )

    if (await session.execute(query)).fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This time slot is already booked')

    auto_confirm = (await session.execute(select(settings.c.auto_confirm))).fetchone()[0]

    booking_status = 'confirmed' if auto_confirm else 'pending'

    start_time = convert_time(booking_request.start_time)
    end_time = convert_time(booking_request.end_time)

    try:
        stmt = insert(booking).values(
            user_id=user.id,
            headset_id=booking_request.headset_id,
            start_time=start_time,
            end_time=end_time,
            status=booking_status
        )
        
        await session.execute(stmt)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

    return {'status': booking_status}
