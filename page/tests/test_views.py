import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_home(client):
    url = reverse("page:home")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_about(client):
    url = reverse("page:about")
    response = client.get(url)
    assert response.status_code == 200
