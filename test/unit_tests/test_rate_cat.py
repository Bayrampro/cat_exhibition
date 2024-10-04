import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Rating, Kind, Cat


@pytest.mark.django_db
def test_rate_cat():
    client = APIClient()
    test_user = User.objects.create_user(username='Bayram', password='12345+')

    refresh = RefreshToken.for_user(test_user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    test_kind = Kind.objects.create(name='Свинкс')

    test_cat = Cat.objects.create(color='#F7822E',
                                  age=3, description='Рыжий кот',
                                  user_id=test_user.pk,
                                  kind_id=test_kind.pk)

    url = reverse('rate_cat', kwargs={'pk': test_cat.pk})

    data = {
        'score': 4,
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['score'] == data['score']

    cat_rating = Rating.objects.get(cat_id=test_cat.pk, user_id=test_user.pk)

    assert cat_rating.score == data['score']
    assert cat_rating.cat == test_cat
