# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY ./app /app/app

# Команда для запуска сервера
# Важно: используем порт, который предоставляет Railway через переменную $PORT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]