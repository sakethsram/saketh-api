import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/GetClients"

@pytest.mark.parametrize("expected_keys", [
    ["client_id", "client_name", "contact", "email", "address"]
])
def test_get_clients(expected_keys):
    response = requests.get(BASE_URL + ENDPOINT)
    assert response.status_code == 200
    
    json_data = response.json()
    assert isinstance(json_data, list)  # Ensure response is a list
    
    for client in json_data:
        assert isinstance(client, dict)  # Each client should be a dict
        for key in expected_keys:
            assert key in client  # Ensure expected keys exist
            assert client[key] is not None  # Ensure values are not None
