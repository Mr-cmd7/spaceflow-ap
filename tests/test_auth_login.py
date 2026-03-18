def test_login_user(client):
    """Тест входа в систему"""
    # Сначала регистрируем пользователя
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    # Пытаемся залогиниться
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Тест входа с неверным паролем"""
    # Регистрируем пользователя
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    # Пытаемся залогиниться с неверным паролем
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrong_password"
    })

    assert response.status_code == 401