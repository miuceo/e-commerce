from django.urls import path
from .views import BlosPageView, BlogDetailView

# Create your views here.

app_name = "blog"

urlpatterns = [
    path('', BlosPageView.as_view(), name='blog'),
    path('blog-details/', BlogDetailView.as_view(), name='blog-detail')
]