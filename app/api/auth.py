from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Аутентификация"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.

    - **email**: должен быть уникальным
    - **password**: минимум 6 символов
    - **full_name**: имя пользователя
    - **phone**: опционально
    """
    # Проверяем, не занят ли email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    # Создаём нового пользователя
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Вход в систему.

    Возвращает JWT токен, который нужно передавать в заголовке:
    `Authorization: Bearer <токен>`
    """
    # Ищем пользователя по email
    user = db.query(User).filter(User.email == user_data.email).first()

    # Проверяем пароль
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем, активен ли пользователь
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь заблокирован"
        )

    # Обновляем время последнего входа
    from datetime import datetime
    user.last_login = datetime.now()
    db.commit()

    # Создаём токен
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем авторизованном пользователе.
    """
    return current_user