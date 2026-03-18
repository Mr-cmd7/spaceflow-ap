from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаём движок PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """
    Функция-генератор для получения сессии БД.
    Используется в зависимостях FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()