from rest_framework import routers
from django.urls import include, path
from .views import UserViewSet, GetTokenView, SignUpViewSet
router = routers.DefaultRouter()


router.register(r'signup', SignUpViewSet, basename='signup')
# router.register(r'token', GetTokenView, basename='get_token')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    
    path('api/v1/auth/', include(router.urls)),
    path('api/v1/auth/token/', GetTokenView.as_view())
    
]
