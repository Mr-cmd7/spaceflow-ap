from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль на соответствие хешу"""
    return check_password_hash(hashed_password, plain_password)


def get_password_hash(password: str) -> str:
    """Создаёт хеш пароля"""
    return generate_password_hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создаёт JWT токен"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Декодирует JWT токен и возвращает данные"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None