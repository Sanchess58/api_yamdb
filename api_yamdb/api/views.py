from django.shortcuts import render
from .models import User
from rest_framework import  viewsets
from .serializers import UserSerializer


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Создание пользователя."""
        serializer.save()


class GetToken(viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    pass