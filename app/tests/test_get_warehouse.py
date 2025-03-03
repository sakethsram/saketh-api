import pytest
import requests

# Base URL of your running FastAPI app
BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.parametrize(
    "headers, expected_status, expected_response",
    [
        ({}, 403, {"detail": "Not authenticated"}),  # ✅ Match actual API response
        ({"Authorization": "Bearer invalid_token"}, 403, {"detail": "Login session expired or invalid session. Please log in again."}),  # ✅ Match actual API response
    ],
)
def test_get_warehouse_list_unauthorized(headers, expected_status, expected_response):
    """Test unauthorized access with missing or invalid token."""
    response = requests.get(f"{BASE_URL}/getWarehouseList", headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response

def test_get_warehouse_list_success():
    """Test case when the API successfully fetches warehouse details."""
    valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2xvZ2luX2lkIjoibGlraGl0YWJlZWthbUBnbWFpbC5jb20iLCJyb2xlcyI6WyJDQVRFR09SWU1BTkFHRVIiXSwiY2xpZW50X2lkIjoxLCJleHAiOjE3NDEwMDE1NjN9.fuwLmdYCak0QG02uqadN8ztBwjrv2RD4Sarp4V5pWH4"  # Replace with an actual valid token
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = requests.get(f"{BASE_URL}/getWarehouseList", headers=headers)

    assert response.status_code == 200
    assert "wareHouseList" in response.json()
    assert isinstance(response.json()["wareHouseList"], list)
