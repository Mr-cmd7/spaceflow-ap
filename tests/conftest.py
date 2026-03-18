import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings
from app.models.room import Room

# Создаём тестовую базу данных в памяти SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределяем зависимость get_db для использования тестовой БД"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента"""
    # Создаём таблицы в тестовой БД
    Base.metadata.create_all(bind=engine)

    # Переопределяем зависимость
    app.dependency_overrides[get_db] = override_get_db

    # Создаём тестового клиента
    with TestClient(app) as test_client:
        yield test_client

    # Очищаем после тестов
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_room(client):
    """Фикстура для создания тестового помещения"""
    # Сначала логинимся как админ (нужно создать админа или использовать прямой доступ к БД)
    # Проще создать помещение напрямую через БД
    db = TestingSessionLocal()
    room = Room(
        name="Тестовое помещение",
        description="Для тестирования",
        capacity=20,
        equipment="Столы, стулья",
        is_active=True
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    db.close()
    return room