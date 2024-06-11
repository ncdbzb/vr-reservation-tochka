from pydantic import EmailStr
from celery import Celery
from datetime import datetime
from src.services.email_service import EmailService
from config.config import REDIS_PORT


celery = Celery('taks', broker=f'redis://redis:{REDIS_PORT}/0', result_backend=f'redis://redis:{REDIS_PORT}/0')

@celery.task
def send_email_task(
    status: str,
    user_email: EmailStr,
    headset_name: str,
    start_time: datetime,
    end_time: datetime,
    cost: int| None = None
) -> str:
    try:
        if status == 'confirmed':
            EmailService.send_confirm_email(user_email, headset_name, start_time, end_time, cost)
        elif status == 'pending':
            EmailService.send_pendign_email(user_email, headset_name, start_time, end_time, cost)
        elif status == 'cancelled':
            EmailService.send_cancel_email(user_email, headset_name, start_time, end_time)
        return 'success'
    except Exception as e:
        print(e)
        return e
    