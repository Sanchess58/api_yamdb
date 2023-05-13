from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    confirmation_code = models.UUIDField("Код подтверждения")


    
