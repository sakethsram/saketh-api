import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2xvZ2luX2lkIjoibGlraGl0YWJlZWthbUBnbWFpbC5jb20iLCJyb2xlcyI6WyJDQVRFR09SWU1BTkFHRVIiXSwiY2xpZW50X2lkIjoxLCJleHAiOjE3NDA5MjcyNDZ9.3abru6z8QSEX2J7OhFwrC8Y3X1FdRhJLFvPRVEIxBBM"

@pytest.mark.parametrize("headers, expected_status, expected_response", [
    ({}, 403, {"detail": "Not authenticated"}),  # ✅ No token (matches updated API)
    ({"Authorization": "Bearer invalid_token"}, 403, {"detail": "Login session expired or invalid session. Please log in again."}),  # ✅ Invalid token (matches updated API)
])
def test_token_validation(headers, expected_status, expected_response):
    """Tests token validation with valid, missing, and invalid tokens."""
    response = requests.get(f"{BASE_URL}/token_validation", headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response
