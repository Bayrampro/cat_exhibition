import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_jwt_token():
    client = APIClient()
    url = reverse('token_obtain_pair')
    test_user = User.objects.create_user(username='Bayram', password='12345+')
    data = {
        'username': test_user.username,
        'password': '12345+',
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_200_OK

    assert 'access' in response.data
    assert 'refresh' in response.data
