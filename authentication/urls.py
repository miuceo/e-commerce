from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("sign-in/", views.signin_view, name="sign-in"),
    path("sign-up/", views.signup_view, name="sign-up"),
    path('logout/', views.logout_view, name='logout')
]
