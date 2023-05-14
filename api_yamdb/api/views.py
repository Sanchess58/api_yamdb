import uuid

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import User

from .permisions import AdminOrReadOnly
from .serializers import TokenSerializer, UserSerializer


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(confirmation_code=uuid.uuid4())
        user = User.objects.get(username=serializer.data.get('username'))

        send_mail(subject='Код подтверждения',
                  message=f'{user.confirmation_code}-код подтверждения',
                  from_email='projectpracticum1@yandex.ru',
                  recipient_list=[user.email],
                  fail_silently=False)


class GetTokenView(TokenObtainPairView):
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

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
