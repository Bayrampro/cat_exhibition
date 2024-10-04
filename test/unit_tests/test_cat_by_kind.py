import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Kind, Cat


@pytest.mark.django_db
def test_cat_by_kind():
    test_kind_1 = Kind.objects.create(name='Свинкс')
    test_kind_2 = Kind.objects.create(name='Амурский')

    test_user = User.objects.create(username='Bayram', password='12345+')
    test_cat_1 = Cat.objects.create(color='#F7822E',
                                    age=2,
                                    description='Красивая',
                                    kind_id=test_kind_2.pk,
                                    user_id=test_user.pk
                                    )
    test_cat_2 = Cat.objects.create(color='#A6A6A6',
                                    age=6,
                                    description='Худая',
                                    kind_id=test_kind_1.pk,
                                    user_id=test_user.pk
                                    )

    client = APIClient()
    url = reverse('cats_by_kind', kwargs={'pk': test_kind_1.pk})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) > 0
    assert response.data[0]['color'] == test_cat_2.color
