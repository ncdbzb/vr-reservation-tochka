from celery import Celery, current_app
from celery.signals import worker_ready
from celery.schedules import crontab
from datetime import datetime, timedelta
from src.utils.convert_time import convert_time
from src.models.bookings import booking
from sqlalchemy import select, and_, update
from config.config import REDIS_URL
from config.database import async_session_maker
import asyncio


celery = Celery('task', broker=REDIS_URL, result_backend=REDIS_URL)

celery.conf.beat_schedule = {
    'cancel-pending-bookings-every-hour': {
        'task': 'src.services.celery_service.cancel_expired_pending_bookings',
        'schedule': crontab(minute=0, hour='*'),
    },
}


@celery.task
def cancel_expired_pending_bookings():
    asyncio.run(cancel_expired_pending_bookings_async())


async def cancel_expired_pending_bookings_async():
    async with async_session_maker() as session:
        delta_time =  convert_time(datetime.now()) - timedelta(hours=1)
        
        query = select(booking).where(
            and_(
                booking.c.status == 'pending',
                booking.c.created_at < delta_time
            )
        )

        pending_bookings = (await session.execute(query)).fetchall()

        for pending_booking in pending_bookings:
            await session.execute(
                update(booking)
                .where(booking.c.id == pending_booking.id)
                .values(status='cancelled')
            )

        await session.commit()
        return {'status': True}
