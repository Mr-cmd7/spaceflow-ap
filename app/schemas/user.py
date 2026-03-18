from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# Базовая схема с общими полями
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = None


# Схема для регистрации (входные данные)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)

    @validator('password')
    def validate_password(cls, v):
        """Обрезает пароль до 72 символов для bcrypt"""
        if len(v.encode('utf-8')) > 72:
            v = v[:72]
        return v


# Схема для ответа (выходные данные) — без пароля!
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Позволяет работать с SQLAlchemy моделями


# Схема для логина
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Схема для данных из токена
class TokenData(BaseModel):
    email: Optional[str] = None