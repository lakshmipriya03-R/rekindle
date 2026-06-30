def test_register_success(client):
    response = client.post("/auth/register", json={
        "full_name": "Alice", "email": "alice@example.com", "password": "password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "alice@example.com"

def test_register_duplicate_email(client):
    payload = {"full_name": "Bob", "email": "bob@example.com", "password": "password123"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409

def test_login_success(client, registered_user):
    response = client.post("/auth/login", json={"email": "test@rekindle.app", "password": "securepass123"})
    assert response.status_code == 200

def test_login_wrong_password(client, registered_user):
    response = client.post("/auth/login", json={"email": "test@rekindle.app", "password": "wrong"})
    assert response.status_code == 401

def test_refresh_token(client, registered_user):
    response = client.post("/auth/refresh", json={"refresh_token": registered_user["refresh_token"]})
    assert response.status_code == 200

def test_get_me(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
