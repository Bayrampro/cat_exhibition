from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('cats/', CatListAPIView.as_view(), name='cats'),
    path('kinds/', KindListAPIView.as_view(), name='kinds'),
    path('cats/<int:pk>/', CatsByKind.as_view(), name='cats_by_kind'),
    path('cat-detail/<int:pk>/', CatDetailAPIView.as_view(), name='cats_detail'),
    path('create-cat/', CatCreateAPIView.as_view(), name='create_cat'),
    path('cat-update/<int:pk>/', CatUpdateAPIView.as_view(), name='cat_update'),
    path('cat-delete/<int:pk>/', CatDeleteAPIView.as_view(), name='cat_delete'),
    path('cats/<int:pk>/rate/', RateCatAPIView.as_view(), name='rate_cat'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]