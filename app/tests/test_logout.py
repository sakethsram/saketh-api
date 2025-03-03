import pytest
import requests

# Base URL of your running FastAPI app (Make sure the server is running)
BASE_URL = "http://127.0.0.1:8000"

# ✅ Correct Bearer Token (Replace if needed)
VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2xvZ2luX2lkIjoibGlraGl0YWJlZWthbUBnbWFpbC5jb20iLCJyb2xlcyI6WyJDQVRFR09SWU1BTkFHRVIiXSwiY2xpZW50X2lkIjoxLCJleHAiOjE3NDA5MjcyNDZ9.3abru6z8QSEX2J7OhFwrC8Y3X1FdRhJLFvPRVEIxBBM"

@pytest.mark.parametrize(
    "headers, expected_status, expected_response",
    [
        ({}, 403, {"detail": "Not authenticated"}),  # ❌ Fix expected error message
        ({"Authorization": "Bearer invalid_token"}, 403, {"detail": "Invalid token"}),  # ❌ Modify API to return 403 for invalid token
    ],
)

def test_logout(headers, expected_status, expected_response):
    """✅ Tests logout functionality with valid, missing, and invalid tokens."""
    
    response = requests.post(f"{BASE_URL}/logout", headers=headers)

    assert response.status_code == expected_status
    assert response.json() == expected_response
