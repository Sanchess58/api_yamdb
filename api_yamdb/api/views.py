from reviews.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token

import uuid
from django.core.mail import EmailMessage, send_mail

class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        serializer.save(confirmation_code = uuid.uuid4())
        user = User.objects.get(username=serializer.data.get('username'))
        
        send_mail(subject='Код подтверждения',
                  message=f'{user.confirmation_code}-код подтверждения',
                  from_email='projectpracticum1@yandex.ru',
                  recipient_list=[user.email],
                  fail_silently=False)
    
        
        
        

class GetToken(viewsets.ModelViewSet):
   queryset = Token.objects.all()
   serializer_class = TokenSerializer

class UserViewSet(viewsets.ModelViewSet):
    pass