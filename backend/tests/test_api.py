import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CodexAtlas API", "version": "1.0.0", "status": "operational"}

def test_rate_limiting():
    # Attempt more than 10 requests to trigger rate limit (configured 10/minute)
    for _ in range(10):
        response = client.get("/")
        assert response.status_code == 200
        
    # The 11th request should be rate-limited
    response = client.get("/")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text
