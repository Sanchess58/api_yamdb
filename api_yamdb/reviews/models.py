from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from reviews.validators import check_future_year


class TimeDateModelMixin(models.Model):
    """Абстрактная модель. Добавляем дату создания."""

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date')

    def __str__(self):
        """Возвращаем укороченный текст модели."""
        return (
            self.text[:settings.ADMINS_TEXT_LENGHT] + '...'
            if len(self.text) >= settings.ADMINS_TEXT_LENGHT
            else self.text
        )


class CategoryGenreModelMixin(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        abstract = True


class Category(CategoryGenreModelMixin):
    """Модель Категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(CategoryGenreModelMixin):
    """Модель Жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        null=True,
        help_text='Год выхода',
        validators=[check_future_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(TimeDateModelMixin):
    """Модель отзывов."""
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите ваш текст!',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв к произведению',
    )
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        help_text='Поставьте оценку от 1 до 10',
        validators=(
            MinValueValidator(
                settings.MIN_SCORE_VALUE,
                'Оценка должна быть не меньше 1!'
            ),
            MaxValueValidator(
                settings.MAX_SCORE_VALUE,
                'Оценка должна быть не больше 10!'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'author',
                    'title',
                ],
                name='unique_author_title',
            )
        ]


class Comment(TimeDateModelMixin):
    """Модель комментариев к отзыву."""
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите ваш текст!',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарии к отзыву',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
