from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import HomePageView

app_name = "api"

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name="token"),
    path('auth/refresh/', TokenRefreshView.as_view(), name="refresh"),
    
    path('', HomePageView.as_view(), name="home")
]

  