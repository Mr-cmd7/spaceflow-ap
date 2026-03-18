from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

# Схема OAuth2 для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """
    Получает текущего пользователя из JWT токена.
    Используется в защищённых эндпоинтах.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Декодируем токен
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # Извлекаем email из токена (хранится в поле "sub")
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Ищем пользователя в базе
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Проверяет, активен ли пользователь.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


def require_role(required_role: str):
    """
    Фабрика зависимостей для проверки роли.
    Использование: Depends(require_role("admin"))
    """

    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав. Требуется роль: " + required_role
            )
        return current_user

    return role_checker