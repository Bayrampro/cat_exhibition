import pytest
from django.urls import reverse
from rest_framework import status

from core.models import Kind
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_kind_list():
    Kind.objects.create(name='Сфинкс')
    Kind.objects.create(name='Амурский')
    Kind.objects.create(name='Дворняга')

    client = APIClient()
    url = reverse('kinds')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert isinstance(response.data, list)
    assert response.data[1]['name'] == 'Амурский'
