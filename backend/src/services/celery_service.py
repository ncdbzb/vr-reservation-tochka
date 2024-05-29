from fastapi import HTTPException
from pydantic import EmailStr
from celery import Celery
from src.services.email_service import EmailService
from config.config import REDIS_PORT


celery = Celery('taks', broker=f'redis://redis:{REDIS_PORT}/0', result_backend=f'redis://redis:{REDIS_PORT}/0')

@celery.task
def send_email_task(user_email: EmailStr):
    try:
        EmailService.send_hello_email(user_email)
        return 'success'
    except Exception as e:
        print(e)
        return e
    