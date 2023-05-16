from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import serializers

from reviews.models import (
    ROLE_CHOICES, Category, Comment,
    Genre, Review, Title, User,
)


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор формы регистрации.
    """

    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise ValidationError({"message": "недопустимый username"})
        return username

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            user = User.objects.get(username=data['username'])
            if user.email == data['email']:
                return data
            raise ValidationError({"message": "Неверный email"})
        return data


class ActivationSerializer(serializers.ModelSerializer):
    """
    Сериализатор получения JWT-токена.
    """

    username = serializers.SlugField(max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            return username
        raise Http404(f'Недопустимое имя пользователя'
                      f'или пользователь `{username}` не найден.')
        # У нас, к сожалению, не получилось вернуть код 404 из сериализатора
        # А тесты требуют именно 404, поэтому чтобы не засорять вьюхи
        # решили реализовать эту логику подобным образом

    def validate(self, data):
        user = User.objects.get(username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            raise ValidationError(
                {"Ошибка": 'Неверный код подтверждения'}
            )
        return data


class AdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор работы администратора с доступом к ролям.
    """

    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User.
    """

    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        read_only_fields = ('username', 'email', 'role',)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории.
    """

    class Meta:
        exclude = ('id', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанра.
    """

    class Meta:
        exclude = ('id', )
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания произведений.
    """

    name = serializers.CharField(
        max_length=200,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            '__all__'
        )


class TitleReciveSerializer(serializers.ModelSerializer):
    """
    Сериализатор получения произведений.
    """

    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description',
        )


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Отзывов.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date',
        )

    def validate_score(self, value):
        """Проверка выставленной оценки в сериализаторе."""
        if not (
            settings.MIN_SCORE_VALUE <= value <= settings.MAX_SCORE_VALUE
        ):
            raise serializers.ValidationError(
                'Оценка может быть только от 1 до 10!'
            )
        return value

    def validate(self, data):
        """Проверяем, что отзыв на произведение не был написан."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title__id=title_id).exists():
            raise serializers.ValidationError('Нельзя дважды писать отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Комментариев.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date',
        )
