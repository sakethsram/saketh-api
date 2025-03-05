from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app
import pytest 
client = TestClient(app)

@pytest.mark.parametrize("user", VALID_USERS)
def test_login_success(user):
    response = client.post("/login", data=user)  # Simulate form data submission
    print(response.text)  # Debugging: Check the actual response
    assert response.status_code == 200
