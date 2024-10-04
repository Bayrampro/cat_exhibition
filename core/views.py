from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions

from .models import Cat, Kind, Rating
from .permissions import IsOwner
from .serializers import CatSerializer, KindSerializer, RatingSerializer


class CatListAPIView(generics.ListAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Список котят',
        responses={
            200: CatSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, *kwargs)


class KindListAPIView(generics.ListAPIView):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Список пород',
        responses={200: KindSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CatsByKind(generics.ListAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Список котят по породам',
        responses={200: CatSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID породы для филтрации котят',
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        kind_id = self.kwargs.get('pk')
        return Cat.objects.filter(kind__pk=kind_id)


class CatDetailAPIView(generics.RetrieveAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description='Детальный просмотр котенка',
        responses={200: CatSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID котенка для детального просмотра',
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CatCreateAPIView(generics.CreateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CatSerializer,
        operation_description='Создает новых котенков',
        responses={201: CatSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Токен авторизации в формате 'Bearer <токен>'",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CatUpdateAPIView(generics.UpdateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_class = [permissions.IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_description="Обновление информации о котенке",
        responses={200: CatSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID котенка для обновления",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Токен авторизации в формате 'Bearer <токен>'",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=CatSerializer
    )
    def patch(self, request, *args, **kwargs):
       return super().patch(request, *args, **kwargs)


class CatDeleteAPIView(generics.DestroyAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_description="Удаление информации о котенке",
        responses={204: openapi.Response(description='Нет содержимого')},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID котенка для удаление",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Токен авторизации в формате 'Bearer <токен>'",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class RateCatAPIView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Дать оценку котенку',
        request_body=RatingSerializer,
        responses={200: RatingSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID Котенка',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Токен авторизации в формате 'Bearer <токен>'",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        cat_id = self.kwargs.get('pk')
        cat = Cat.objects.get(id=cat_id)

        serializer.save(user=self.request.user, cat=cat)