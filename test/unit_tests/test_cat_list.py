import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from core.models import Cat, Kind


@pytest.mark.django_db
def test_cat_list():
    kind = Kind.objects.create(name='Сфинкс')
    user = User.objects.create(username='Bayram', password='12345+')
    cat = Cat.objects.create(color='#F7822E', age=2, description='Красивая', kind_id=kind.pk, user_id=user.pk)
    client = APIClient()
    url = reverse('cats')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) > 0
    assert response.data[0]['color'] == cat.color
