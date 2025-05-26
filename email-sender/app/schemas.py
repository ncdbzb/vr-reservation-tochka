from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    user_email: EmailStr
    subject: str
    body: str
