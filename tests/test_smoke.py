from django.test import Client


def test_smoke_root():
    client = Client()
    response = client.get("/")
    assert response.status_code in (200, 301, 302)
