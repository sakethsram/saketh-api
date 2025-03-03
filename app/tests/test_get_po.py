import pytest
import requests
import os

# Base URL of your running FastAPI app
BASE_URL = "http://127.0.0.1:8000"

# Fetch the valid token from the environment
VALID_TOKEN = os.getenv("VALID_TOKEN")

@pytest.mark.parametrize(
    "params, expected_status",
    [
        ({"pageSize": 10, "pageNumber": 1}, 200),
        ({"pageSize": 5, "pageNumber": 1, "poNumber": "PO12345"}, 200),
        ({"pageSize": 10, "pageNumber": 1, "status": "Pending"}, 200),
        ({"pageSize": 10, "pageNumber": 1, "startDate": "2024-03-01", "endDate": "2024-03-10"}, 200),
        ({"pageSize": 0, "pageNumber": 1}, 422),  # Invalid pageSize
    ],
)
def test_po_listing(params, expected_status):
    """Test /poListing endpoint with various parameters."""
    if not VALID_TOKEN:
        pytest.skip("VALID_TOKEN is not set in environment variables.")
    
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    response = requests.get(f"{BASE_URL}/poListing", headers=headers, params=params)
    
    assert response.status_code == expected_status
