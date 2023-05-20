from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = settings.USER
    ADMIN = settings.ADMIN
    MODERATOR = settings.MODERATOR


class User(AbstractUser):
    """Модель Юзера."""

    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=UserRole.choices,
        default=settings.USER,
        help_text='Выберете роль пользователя'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_user(self):
        return self.role == settings.USER

    @property
    def is_admin(self):
        return self.role == settings.ADMIN

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
