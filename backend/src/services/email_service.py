from datetime import datetime
from fastapi import HTTPException
import httpx
from pydantic import EmailStr

from config.config import EMAIL_SENDER_URL


class EmailService:
    @staticmethod
    def send_email(user_email: str, subject: str, body: str):
        try:
            payload = {
                "user_email": user_email,
                "subject": subject,
                "body": body
            }
            response = httpx.post(f'{EMAIL_SENDER_URL}/send-email', json=payload, timeout=10)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Email service error: {response.text}")
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    @classmethod
    def send_confirm_email(cls, user_email: str, headset_name: str,
                           start_time: datetime, end_time: datetime, cost: int):
        subject = 'Бронирование подтверждено'
        body = (f'<div>'
                f'<h1>Здравствуйте, Ваше бронирование было успешно подтверждено!</h1>'
                f'<p><b>Детали бронирования:</b><br>'
                f'Название VR шлема: {headset_name}<br>'
                f'Дата и время начала: {start_time}<br>'
                f'Дата и вермя окончания: {end_time}<br>'
                f'Стоимость: {cost} руб.</p>'
                f'</div>')
        cls.send_email(user_email, subject, body)

    @classmethod
    def send_pendign_email(cls, user_email: str, headset_name: str,
                           start_time: datetime, end_time: datetime, cost: int):
        subject = 'Бронирование ожидает подтверждения'
        body = (f'<div>'
                f'<h1>Здравствуйте, мы получили Вашу заявку! В ближайшее время администратор её проверит.</h1>'
                f'<p><b>Детали бронирования:</b><br>'
                f'Название VR шлема: {headset_name}<br>'
                f'Дата и время начала: {start_time}<br>'
                f'Дата и вермя окончания: {end_time}<br>'
                f'Стоимость: {cost} руб.</p>'
                f'</div>')
        cls.send_email(user_email, subject, body)

    @classmethod
    def send_cancel_email(cls, user_email: str, headset_name: str,
                          start_time: datetime, end_time: datetime):
        subject = 'Бронирование отменено'
        body = (f'<div>'
                f'<h1>Здравствуйте, Ваше бронирование было отклонено.</h1>'
                f'<p>Вы оставляли заявку на бронирование {headset_name} с {start_time} по {end_time}.<br>'
                f'Данное бронирование было отменено.</p>'
                f'</div>')
        cls.send_email(user_email, subject, body)

    @classmethod
    def send_notice_email(cls, user_email: str, headset_name: str, old_cost: int, new_cost: int):
        subject = 'Снижение цен на бронирования'
        body = (f'<div>'
                f'<h1>Здравствуйте, цена на {headset_name} бронирование снизилась!</h1>'
                f'<p>Старая цена: <s>{old_cost}</s><br>'
                f'Новая цена: <b>{new_cost}</b></p>'
                f'</div>')
        cls.send_email(user_email, subject, body)


def send_email_task(
    status: str,
    user_email: EmailStr,
    headset_name: str,
    start_time: datetime,
    end_time: datetime,
    cost: int | None = None,
    old_cost: int | None = None,
) -> str:
    try:
        if status == 'confirmed':
                EmailService.send_confirm_email(user_email, headset_name, start_time, end_time, cost)
        elif status == 'pending':
                EmailService.send_pendign_email(user_email, headset_name, start_time, end_time, cost)
        elif status == 'cancelled':
                EmailService.send_cancel_email(user_email, headset_name, start_time, end_time)
        elif status == 'notice':
                EmailService.send_notice_email(user_email, headset_name, old_cost, cost)
        return 'success'
    except Exception as e:
        raise e

