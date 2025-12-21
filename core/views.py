from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'index.html'
    
class AboutPageView(TemplateView):
    template_name = 'about.html'
    
class ShopPageView(TemplateView):
    template_name = 'shop.html'
    
class CartPageView(TemplateView):
    template_name = 'shopping-cart.html'
    
