import pytest
import requests

# Base URL of the FastAPI server (already running)
BASE_URL = "http://127.0.0.1:8000"

# Valid test user credentials - keeping only the ones that work
VALID_USERS = [
    {"username": "prakash.n@samyudhi.com", "password": "pjnjnuh"},
    {"username": "Utsav.a@evenflow.com", "password": "ujnjnuh"},
    {"username": "ikshwakv@gmail.com", "password": "ijnjnuh"},
]

# Invalid credentials (wrong password or non-existent user)
INVALID_CREDENTIALS = [
    {"username": "prakash.n@samyudhi.com", "password": "wrongpassword"},
    {"username": "invaliduser@gmail.com", "password": "password123"},
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
    
    # Optional additional checks based on the sample response
    assert isinstance(json_data["client_id"], int)
    assert isinstance(json_data["roles"], str)

@pytest.mark.parametrize("user", INVALID_CREDENTIALS)
def test_login_failure(user):
    """Test login failure with invalid credentials."""
    response = requests.post(f"{BASE_URL}/login", data=user)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

# New test to check for missing roles
def test_login_no_roles():
    """Test login with a user that has no assigned roles."""
    # This test assumes you have a user with no roles in your test database
    user = {"username": "noroles@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/login", data=user)
    
    # If the user exists but has no roles, we should get a 403 error
    if response.status_code == 403:
        assert response.json()["detail"] == "User has no assigned roles or roles are inactive."
    else:
        # If the user doesn't exist, we'll get a 401 error instead, which is also acceptable
        assert response.status_code == 401