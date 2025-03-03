import os
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

# Fetch the token from the environment
VALID_TOKEN = os.getenv("VALID_TOKEN")

@pytest.mark.parametrize("headers, expected_status, expected_response", [
    ({}, 403, {"detail": "Not authenticated"}),  # No token case
    ({"Authorization": "Bearer invalid_token"}, 403, {"detail": "Login session expired or invalid session. Please log in again."}),  # Invalid token case
    ({"Authorization": f"Bearer {VALID_TOKEN}"}, 200, {"is_token_valid": "yes"}),  # Valid token case
])
def test_token_validation(headers, expected_status, expected_response):
    response = requests.get(f"{BASE_URL}/token_validation", headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response
