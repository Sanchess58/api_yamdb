from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    confirmation_code = models.TextField("Код подтверждения")
