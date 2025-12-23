from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePageView( TemplateView):
    template_name = 'index.html'
    login_url = '/auth/sign-in/'

class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
    login_url = '/auth/sign-in/'

class ShopPageView(LoginRequiredMixin, TemplateView):
    template_name = 'shop.html'
    login_url = '/auth/sign-in/'

class ShopDetailsPageView(LoginRequiredMixin, TemplateView):
    template_name = 'shop-details.html'
    login_url = '/auth/sign-in/'

class CartPageView(LoginRequiredMixin, TemplateView):
    template_name = 'shopping-cart.html'
    login_url = '/auth/sign-in/'

class CheckoutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'
    login_url = '/auth/sign-in/'

class ContactPageView(LoginRequiredMixin, TemplateView):
    template_name = 'contact.html'
    login_url = '/auth/sign-in/'
