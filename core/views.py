from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from blog.models import Blog

# Create your views here.

class HomePageView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()[:4]
        data['blogs'] = Blog.objects.all()[:4]
        
        return data

from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category, Brand, Size

class ShopPageView(LoginRequiredMixin, ListView):
    template_name = 'shop.html'
    login_url = '/auth/sign-in/'
    model = Product
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        category_slug = self.request.GET.get('category')
        brand_slug = self.request.GET.get('brand')
        price = self.request.GET.get('price')
        size_id = self.request.GET.get('size')

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(desc__icontains=q)
            )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)

        if size_id:
            queryset = queryset.filter(sizes__id=size_id)


        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        data['sizes'] = Size.objects.all()
        data['brands'] = Brand.objects.all()
    
        data['selected_category'] = self.request.GET.get('category')
        data['selected_brand'] = self.request.GET.get('brand')
        data['selected_price'] = self.request.GET.get('price')
        data['selected_size'] = self.request.GET.get('size')
        data['search_query'] = self.request.GET.get('q', '')
        return data

class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
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
