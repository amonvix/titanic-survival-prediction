import pytest
from django.test import Client


@pytest.mark.django_db
def test_smoke_root():
    client = Client()
    response = client.get("/")
    assert response.status_code in (200, 301, 302)
