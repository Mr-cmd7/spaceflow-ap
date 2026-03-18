def test_cancel_booking(client, test_room):
    """Тест отмены бронирования"""
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

    # 2. Создаём бронь
    from datetime import datetime, timedelta
    start_time = (datetime.now() + timedelta(days=1)).isoformat()
    end_time = (datetime.now() + timedelta(days=1, hours=2)).isoformat()

    create_response = client.post(
        "/api/bookings/",
        json={
            "room_id": test_room.id,
            "start_time": start_time,
            "end_time": end_time,
            "purpose": "Встреча"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 201
    booking_id = create_response.json()["id"]

    # 3. Отменяем бронь
    cancel_response = client.put(
        f"/api/bookings/{booking_id}/cancel",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert cancel_response.status_code == 200
    data = cancel_response.json()
    assert data["status"] == "cancelled"