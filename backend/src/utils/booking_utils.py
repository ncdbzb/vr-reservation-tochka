from fastapi import status, HTTPException
from src.models.headsets import headset
from src.models.bookings import booking
from src.schemas.user_schema import UserSchema
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_headset_name(headset_id: int, session: AsyncSession) -> str:
        query = select(headset.c.name).where(headset.c.id == headset_id)
        return (await session.execute(query)).fetchone()[0]


async def change_booking_status(booking_id: int, session: AsyncSession, user: UserSchema, booking_status: str) -> None:
    query = select(
        booking
    ).where(
        booking.c.id == booking_id,
    )
    my_booking = (await session.execute(query)).fetchone()

    if not my_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')
    if not user.is_superuser and my_booking.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    if my_booking.status == booking_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Booking is already {booking_status}')
    
    stmt = update(
        booking
    ).where(
        booking.c.id == booking_id,
    ).values(
        status=booking_status
    )

    await session.execute(stmt)
    await session.commit()

    return
