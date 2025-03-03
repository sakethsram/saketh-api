import pytest
import requests

# Base URL of the FastAPI server (already running)
BASE_URL = "http://127.0.0.1:8000"

# Valid test user credentials
VALID_USERS = [
    {"username": "prakash.n@samyudhi.com", "password": "pjnjnuh"},
    {"username": "Utsav.a@evenflow.com", "password": "ujnjnuh"},
    {"username": "ikshwakv@gmail.com", "password": "ijnjnuh"},
]

# Invalid credentials (wrong password or non-existent user)
INVALID_CREDENTIALS = [
    {"username": "prakash.n@samyudhi.com", "password": "wrongpassword"},
    {"username": "invaliduser@gmail.com", "password": "pjnjnuh"},
]

@pytest.mark.parametrize("user", VALID_USERS)
def test_login_success(user):
    """Test successful login with valid credentials."""
    response = requests.post(f"{BASE_URL}/login", data=user)

    assert response.status_code == 200
    json_data = response.json()

    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"
    assert "roles" in json_data
    assert "client_id" in json_data
    assert "user_full_name" in json_data

@pytest.mark.parametrize("user", INVALID_CREDENTIALS)
def test_login_failure(user):
    """Test login failure with invalid credentials."""
    response = requests.post(f"{BASE_URL}/login", data=user)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
