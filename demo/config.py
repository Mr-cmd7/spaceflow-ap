"""
Настройки демонстрационного приложения
"""
import os

# URL бэкенда (можно переопределить через переменные окружения)
API_URL = os.getenv("SPACEFLOW_API_URL", "http://localhost:8000/api")

# Настройки приложения
APP_TITLE = "SpaceFlow API Demo"
APP_ICON = "🚀"
APP_LAYOUT = "wide"

# Константы для статусов бронирований (с эмодзи)
BOOKING_STATUS = {
    "pending": "⏳ Ожидает",
    "confirmed": "✅ Подтверждено",
    "rejected": "❌ Отклонено",
    "cancelled": "🚫 Отменено",
    "completed": "✔️ Завершено"
}