from rest_framework import routers
from django.urls import include, path
from .views import UserViewSet, GetToken, SignUpViewSet
router = routers.DefaultRouter()


router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'token', GetToken, basename='get_token')
router.register(r'users', UserViewSet, basename='users')
urlpatterns = [
    
    path('api/v1/auth/', include(router.urls))
    
    
]
