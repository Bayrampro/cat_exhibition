import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Cat, Kind


@pytest.mark.django_db
def test_cats_detail():
    test_kind = Kind.objects.create(name='Свинкс')
    test_user = User.objects.create(username='Bayram', password='12345+')
    test_cat = Cat.objects.create(color='#F7822E',
                                  age=2,
                                  description='Красивая',
                                  kind_id=test_kind.pk,
                                  user_id=test_user.pk)

    client = APIClient()
    url = reverse('cats_detail', kwargs={'pk': test_cat.pk})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert response.data['color'] == test_cat.color
