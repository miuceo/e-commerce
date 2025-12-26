from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, HomePageView, UserRegister
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', UserRegister, basename='register-user')

app_name = "api"

urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name="token"),
    path('auth/refresh/', TokenRefreshView.as_view(), name="refresh"),
    
    path('', HomePageView.as_view(), name="home"),
    *router.urls
]

  