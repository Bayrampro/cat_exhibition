import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_refresh_token():
    client = APIClient()
    get_token_url = reverse('token_obtain_pair')
    refresh_url = reverse('token_refresh')
    test_user = User.objects.create_user(username='Bayram', password='12345+')
    get_token_data = {
        'username': test_user.username,
        'password': '12345+',
    }

    get_token_response = client.post(get_token_url, data=get_token_data)

    refresh_data = {
        'refresh': get_token_response.data['refresh'],
    }

    refresh_response = client.post(refresh_url, data=refresh_data)

    assert refresh_response.status_code == status.HTTP_200_OK

    assert 'access' in refresh_response.data
