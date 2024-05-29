from fastapi import HTTPException
import smtplib
from smtplib import SMTPAuthenticationError
from email.message import EmailMessage

from config.config import SMTP_PASSWORD, SMTP_USER, SMTP_HOST, SMTP_PORT


class EmailService:
    @staticmethod
    def send_email(user_email: str, subject: str, body: list[str]):
        email = EmailMessage()
        email['Subject'] = subject
        email['From'] = SMTP_USER
        email['To'] = user_email

        email.set_content(body, subtype='html')
        try:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(email)
        except SMTPAuthenticationError:
            raise HTTPException(status_code=500, detail='SMTP configuration not set or invalid')

    @classmethod
    def send_hello_email(cls, user_email: str):
        subject = 'hello'
        body = ('<div>'
                '<h1>Здравствуйте!</h1>'
                '<p>Мы получили Вашу заявку! В ближайшее время администратор её проверит, и Вы получите ответ.</p>'
                '</div>')

        cls.send_email(user_email, subject, body)
