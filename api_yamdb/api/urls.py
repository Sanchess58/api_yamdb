from django.urls import include, path
from rest_framework import routers

from .views import GetTokenView, SignUpViewSet, UserViewSet

router = routers.DefaultRouter()


router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'users', UserViewSet, basename='admin_users')


urlpatterns = [
    path('api/v1/auth/', include(router.urls)),
    path('api/v1/auth/token/', GetTokenView.as_view()),
]
