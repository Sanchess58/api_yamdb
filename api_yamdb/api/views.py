from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
import uuid
from api.filters import TitleFilter
from api.mixins import ModelMixinSet
from api.permissions import (
    StaffOrReadOnly, AuthorOrStaffOrReadOnly
)
from api.serializers import ( CategorySerializer,
    CommentSerializer, GenreSerializer, ReviewsSerializer,
    SignUpSerializer, TitleCreateSerializer,
    TitleReciveSerializer
)
from reviews.models import (
    Category, Genre, Review, Title, User,
)


class SignUpViewSet(viewsets.ModelViewSet):
    """Класс регистрации пользователя."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        serializer.save(confirmation_code=uuid.uuid4())
        user = User.objects.get(username=serializer.data.get('username'))

        send_mail(subject='Код подтверждения',
                  message=f'{user.confirmation_code}-код подтверждения',
                  from_email='projectpracticum1@yandex.ru',
                  recipient_list=[user.email],
                  fail_silently=False)


class GetTokenView(TokenObtainPairView):
    """Класс получения токена."""

    serializer_class = TokenSerializer

    def post(self, request):
        user = User.objects.get(username=request.data.get('username'))

        if (
            request.data.get('confirmation_code')
            == str(user.confirmation_code)
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response("Неверный код", status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
    """Класс работы с пользователем."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[
            IamOrReadOnly
        ]
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ModelMixinSet):
    """
    Получить список всех категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (StaffOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """
    Получить список всех жанров.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (StaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех произведений.
    """

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (StaffOrReadOnly,)
    serializer_class = TitleReciveSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews_title__score'))

    def get_serializer_class(self):
        """
        Переопределяем метод get_serializer_class()
        для проверки какаяоперация REST
        была использована и возвращаем серриализаторы
        для записи и чтения.
        """
        if self.action in ['list', 'retrieve']:
            return TitleReciveSerializer
        return TitleCreateSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Отзывов.
    """

    serializer_class = ReviewsSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_title(self):
        """Получаем произведение для отзыва."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получаем queryset."""
        return self.get_title().reviews_title.all()

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(title=self.get_title(), author=self.request.user,)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_review(self):
        """Получаем отзыв для комментария."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Получаем queryset."""
        return self.get_review().comments_review.all()

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(review=self.get_review(), author=self.request.user)
