def test_create_booking_success(client, test_room):
    """Тест успешного создания бронирования"""
    # 1. Регистрируем пользователя
    user_response = client.post("/api/auth/register", json={
        "email": "user@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    # 2. Логинимся и получаем токен
    login_response = client.post("/api/auth/login", json={
        "email": "user@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 3. Создаём бронирование (используем test_room.id)
    from datetime import datetime, timedelta
    start_time = (datetime.now() + timedelta(days=1)).isoformat()
    end_time = (datetime.now() + timedelta(days=1, hours=2)).isoformat()

    response = client.post(
        "/api/bookings/",
        json={
            "room_id": test_room.id,  # Используем реальный ID
            "start_time": start_time,
            "end_time": end_time,
            "purpose": "Встреча",
            "participants_count": 5
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["room_id"] == test_room.id
    assert data["status"] == "pending"
    assert data["user_id"] == user_response.json()["id"]
    assert "id" in data