#!/usr/bin/env python
"""
Скрипт для наполнения базы данных тестовыми данными.
Запуск: python seed_db.py
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

# Добавляем корень проекта в путь, чтобы импортировать модели и настройки
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.models import User, Room, Booking


def seed_database():
    print("🚀 Начало наполнения базы данных тестовыми данными...")

    # Подключение к базе
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Проверяем, есть ли уже пользователи
        if db.query(User).count() > 0:
            print("⚠️  В базе уже есть пользователи. Пропускаем создание.")
        else:
            print("👤 Создание пользователей...")

            # Обычный пользователь
            user1 = User(
                email="user@example.com",
                password_hash=generate_password_hash("password123"),
                full_name="Иван Петров",
                phone="+79991234567",
                role="user",
                is_active=True
            )
            db.add(user1)

            # Администратор
            admin = User(
                email="admin@example.com",
                password_hash=generate_password_hash("admin123"),
                full_name="Мария Админова",
                phone="+79997654321",
                role="admin",
                is_active=True
            )
            db.add(admin)

            db.commit()
            print("✅ Пользователи созданы.")

        # Проверяем, есть ли помещения
        if db.query(Room).count() > 0:
            print("⚠️  Помещения уже есть. Пропускаем.")
        else:
            print("🏢 Создание помещений...")

            rooms = [
                Room(
                    name="Коворкинг",
                    description="Открытое пространство для работы с ноутбуком. Есть столы, стулья, розетки и Wi-Fi.",
                    capacity=30,
                    equipment="Столы, стулья, розетки, Wi-Fi",
                    is_active=True
                ),
                Room(
                    name="Большой концертный зал",
                    description="Просторный зал со сценой, световым и звуковым оборудованием.",
                    capacity=100,
                    equipment="Сцена, свет, звук, микрофоны",
                    is_active=True
                ),
                Room(
                    name="Зал бочки",
                    description="Помещение с уникальной акустикой, подходит для репетиций музыкальных групп.",
                    capacity=15,
                    equipment="Акустическая обработка, музыкальное оборудование (по запросу)",
                    is_active=True
                ),
                Room(
                    name="Зеркальный зал",
                    description="Зал с зеркалами и хореографическим станком. Идеален для танцев, йоги, фитнеса.",
                    capacity=20,
                    equipment="Зеркала, станок, коврики",
                    is_active=True
                ),
                Room(
                    name="Кухня",
                    description="Оборудованная кухня для проведения кулинарных мастер-классов.",
                    capacity=15,
                    equipment="Плита, духовка, холодильник, посуда",
                    is_active=True
                ),
                Room(
                    name="Медиа-студия",
                    description="Профессиональная студия для фото- и видеосъёмки, записи подкастов.",
                    capacity=8,
                    equipment="Софтбоксы, хромакей, микрофоны, камеры",
                    is_active=True
                )
            ]

            for room in rooms:
                db.add(room)

            db.commit()
            print(f"✅ Создано {len(rooms)} помещений.")

        # Проверяем, есть ли бронирования
        if db.query(Booking).count() > 0:
            print("⚠️  Бронирования уже есть. Пропускаем.")
        else:
            print("📅 Создание тестовых бронирований...")

            # Получаем пользователей и помещения
            user = db.query(User).filter(User.email == "user@example.com").first()
            admin = db.query(User).filter(User.email == "admin@example.com").first()
            rooms = db.query(Room).all()

            if not user or not admin or len(rooms) < 3:
                print("❌ Недостаточно данных для создания бронирований.")
                return

            now = datetime.now()

            # Бронирования с разными статусами
            bookings = [
                # pending (ожидание) – завтра
                Booking(
                    user_id=user.id,
                    room_id=rooms[0].id,
                    start_time=now + timedelta(days=1, hours=10),
                    end_time=now + timedelta(days=1, hours=12),
                    status="pending",
                    purpose="Встреча команды",
                    participants_count=5,
                    notes="Обсуждение нового проекта"
                ),
                # confirmed (подтверждено) – послезавтра
                Booking(
                    user_id=user.id,
                    room_id=rooms[1].id,
                    start_time=now + timedelta(days=2, hours=14),
                    end_time=now + timedelta(days=2, hours=16),
                    status="confirmed",
                    purpose="Репетиция концерта",
                    participants_count=10,
                    notes="Нужен звук"
                ),
                # rejected (отклонено) – через 3 дня
                Booking(
                    user_id=user.id,
                    room_id=rooms[2].id,
                    start_time=now + timedelta(days=3, hours=9),
                    end_time=now + timedelta(days=3, hours=11),
                    status="rejected",
                    purpose="Занятие по вокалу",
                    participants_count=1,
                    notes="Администратор отклонил по техническим причинам"
                ),
                # cancelled (отменено пользователем) – через 4 дня
                Booking(
                    user_id=user.id,
                    room_id=rooms[3].id,
                    start_time=now + timedelta(days=4, hours=18),
                    end_time=now + timedelta(days=4, hours=20),
                    status="cancelled",
                    purpose="Йога",
                    participants_count=8,
                    notes="Отменили из-за болезни инструктора"
                ),
                # completed (завершено) – вчера
                Booking(
                    user_id=admin.id,
                    room_id=rooms[4].id,
                    start_time=now - timedelta(days=1, hours=12),
                    end_time=now - timedelta(days=1, hours=14),
                    status="completed",
                    purpose="Кулинарный мастер-класс",
                    participants_count=12,
                    notes="Прошло отлично"
                ),
                # ещё одно pending от admin
                Booking(
                    user_id=admin.id,
                    room_id=rooms[5].id,
                    start_time=now + timedelta(days=2, hours=10),
                    end_time=now + timedelta(days=2, hours=12),
                    status="pending",
                    purpose="Съёмка промо-ролика",
                    participants_count=4,
                    notes="Нужен оператор"
                ),
            ]

            for booking in bookings:
                db.add(booking)

            db.commit()
            print(f"✅ Создано {len(bookings)} бронирований.")

        print("\n🎉 База данных успешно наполнена тестовыми данными!")
        print("   Пользователи:")
        print("     - user@example.com / password123 (обычный пользователь)")
        print("     - admin@example.com / admin123 (администратор)")
        print("   Помещения и бронирования созданы.")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()