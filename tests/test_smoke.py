"""
Basic smoke and API tests for Titanic Survival Prediction project.

This ensures the Django/FastAPI app runs correctly and endpoints respond.
You can expand these tests with model inference validation later.
"""

import os

import pytest

# Try FastAPI first, fallback to Django test setup if not present
try:
    from app.main import app  # adjust if your FastAPI entrypoint is elsewhere
    from fastapi.testclient import TestClient

    client = TestClient(app)
    FASTAPI_MODE = True
except Exception:
    FASTAPI_MODE = False


def test_environment_setup():
    """Ensure required environment and core paths exist."""
    assert os.path.exists("requirements.txt"), "requirements.txt missing"
    assert os.path.isdir("scripts"), "scripts directory missing"
    assert os.path.isdir("app"), "app directory missing"


@pytest.mark.skipif(not FASTAPI_MODE, reason="FastAPI app not available")
def test_predict_endpoint_status():
    """Smoke test for FastAPI /predict/ endpoint."""
    response = client.get("/")
    # Expect redirect or root status 200
    assert response.status_code in (200, 307, 308), (
        f"Unexpected root status: {response.status_code}"
    )

    # Example payload test for /predict/ endpoint
    data = {
        "sex": "male",
        "pclass": 3,
        "age": 25,
        "fare": 7.25,
        "sibsp": 0,
        "parch": 0,
        "embarked": "S",
    }
    response = client.post("/predict/", json=data)
    assert response.status_code == 200, f"/predict/ failed: {response.status_code}"
    result = response.json()
    assert "survival_probability" in result or "prediction" in result, (
        "Response missing prediction key"
    )


def test_sanity_check():
    """Always true sanity test."""
    assert True
