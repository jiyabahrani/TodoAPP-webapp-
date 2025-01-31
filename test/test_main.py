from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

clint = TestClient(app)

def test_return_health_check():
    response = clint.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}