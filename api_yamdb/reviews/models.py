from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES_CHOICES = [
        ("user", "Пользователь"), 
        ("moderator","Модератор"), 
        ("admin", "Администратор")
    ]
    confirmation_code = models.UUIDField("Код подтверждения", blank=True, null=True)
    bio = models.CharField("Биография", blank=True, default="Описание отсутсвует", max_length=256)
    role = models.CharField("Роль", default="user", choices=ROLES_CHOICES, max_length=9)

    