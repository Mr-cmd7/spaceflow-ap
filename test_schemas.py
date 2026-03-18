print("Проверка схем...")

try:
    from app.schemas import UserCreate, UserResponse, RoomCreate, RoomResponse, BookingCreate, BookingResponse
    print("✅ Все схемы импортируются")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("Проверка завершена!")