from rest_framework import routers
from django.urls import include, path
from .views import UserViewSet, GetToken, SignUpViewSet
router = routers.DefaultRouter()


router.register(r'signup', SignUpViewSet, basename='signup')
urlpatterns = [
    
    path('v1/auth/', include(router.urls))
    
    
]
