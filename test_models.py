print("Проверка моделей...")

try:
    from app.models import User, Room, Booking
    print("✅ Все модели импортируются")
except Exception as e:
    print(f"❌ Ошибка импорта моделей: {e}")

print("Проверка завершена!")