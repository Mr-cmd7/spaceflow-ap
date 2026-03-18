def test_create_booking_conflict(client, test_room):
    """Тест попытки создать бронь на уже занятое время"""
    # 1. Регистрируем пользователя
    client.post("/api/auth/register", json={
        "email": "user@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    login_response = client.post("/api/auth/login", json={
        "email": "user@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # 2. Создаём первую бронь
    from datetime import datetime, timedelta
    start_time = (datetime.now() + timedelta(days=1)).isoformat()
    end_time = (datetime.now() + timedelta(days=1, hours=2)).isoformat()

    response1 = client.post(
        "/api/bookings/",
        json={
            "room_id": test_room.id,
            "start_time": start_time,
            "end_time": end_time,
            "purpose": "Первая встреча"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response1.status_code == 201

    # 3. Пытаемся создать вторую бронь на то же время
    response2 = client.post(
        "/api/bookings/",
        json={
            "room_id": test_room.id,
            "start_time": start_time,
            "end_time": end_time,
            "purpose": "Вторая встреча"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response2.status_code == 409
    data = response2.json()
    assert "detail" in data