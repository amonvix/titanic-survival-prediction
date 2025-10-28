from app.routers.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_predict_endpoint_returns_200():
    payload = {
        "age": 28,
        "sex": "male",
        "pclass": 3,
        "sibsp": 0,
        "parch": 0,
        "fare": 7.25,
        "embarked": "Southampton",
        "deck": "Unknown",
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "survived" in body
    assert "survived_probability" in body
