import smtplib
import logging
from email.message import EmailMessage
from fastapi import HTTPException
import os

logger = logging.getLogger(__name__)

# Загрузка переменных окружения
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))


class EmailService:
    @staticmethod
    def send(user_email: str, subject: str, body: str) -> None:
        if not all([SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT]):
            logger.error("SMTP credentials are not fully set in environment variables.")
            raise HTTPException(status_code=500, detail="SMTP configuration is incomplete")

        # Формируем email
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = SMTP_USER
        email["To"] = user_email
        email.set_content(body, subtype="html")

        try:
            # Устанавливаем защищённое соединение и отправляем письмо
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(email)

        except smtplib.SMTPAuthenticationError as e:
            logger.exception("SMTP authentication failed")
            raise HTTPException(status_code=500, detail="SMTP authentication failed")

        except smtplib.SMTPException as e:
            logger.exception("SMTP general error")
            raise HTTPException(status_code=500, detail="Email service error")

        except Exception as e:
            logger.exception("Unexpected error while sending email")
            raise HTTPException(status_code=500, detail="Unexpected error while sending email")
