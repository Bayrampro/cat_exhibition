import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Kind


@pytest.mark.django_db
def test_cat_create():
    client = APIClient()
    url = reverse('create_cat')
    test_kind = Kind.objects.create(name='Свинкс')
    test_user = User.objects.create(username='Bayram', password='12345+')
    refresh = RefreshToken.for_user(test_user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    data = {
        'color': '#A6A6A6',
        'age': 6,
        'description': 'Худая',
        'kind_id': test_kind.pk,
        'user_id': test_user.pk,
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['color'] == data['color']