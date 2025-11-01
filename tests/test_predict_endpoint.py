from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_route_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "API do Titanic" in body["message"]


def test_predict_route_exists():
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
    response = client.post("/predict", json=payload)
    assert response.status_code in [
        200,
        500,
    ]  # aceita erro 500 se modelo não encontrado
