def test_register_user(client):
    """Тест регистрации нового пользователя"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
        "phone": "+79991234567"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "password" not in data  # пароль не должен возвращаться!


def test_register_existing_email(client):
    """Тест попытки регистрации с уже существующим email"""
    # Сначала создаём пользователя
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    # Пытаемся создать ещё одного с таким же email
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "another_password",
        "full_name": "Another User"
    })

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data