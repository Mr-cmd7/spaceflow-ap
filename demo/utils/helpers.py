"""
Вспомогательные функции для демонстрационного приложения
"""
from datetime import datetime
from typing import Dict, Any

def format_datetime(dt_str: str) -> str:
    """Форматирование даты и времени для отображения"""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%d.%m.%Y %H:%M')
    except:
        return dt_str

def format_date(dt_str: str) -> str:
    """Форматирование только даты"""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%d.%m.%Y')
    except:
        return dt_str

def format_time(dt_str: str) -> str:
    """Форматирование только времени"""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%H:%M')
    except:
        return dt_str

def get_status_icon(status: str, status_icons: Dict[str, str]) -> str:
    """Получение иконки для статуса"""
    return status_icons.get(status, status)