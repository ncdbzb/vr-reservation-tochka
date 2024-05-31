from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_active: bool | None = True
    is_superuser: bool | None = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
