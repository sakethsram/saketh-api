import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/GetClients"
VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2xvZ2luX2lkIjoibGlraGl0YWJlZWthbUBnbWFpbC5jb20iLCJyb2xlcyI6WyJDQVRFR09SWU1BTkFHRVIiXSwiY2xpZW50X2lkIjoxLCJleHAiOjE3NDEwMDE1NjN9.fuwLmdYCak0QG02uqadN8ztBwjrv2RD4Sarp4V5pWH4"  # Replace with a working token

@pytest.mark.parametrize(
    "headers, expected_status, expected_response",
    [
        ({}, 403, {"detail": "Not authenticated"}),  
        ({"Authorization": "Bearer invalid_token"}, 403, {"detail": "Login session expired or invalid session. Please log in again."}),  
    ],
)
def test_get_clients_unauthorized(headers, expected_status, expected_response):
    """Test unauthorized access with missing or invalid tokens."""
    response = requests.get(f"{BASE_URL}{ENDPOINT}", headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response
