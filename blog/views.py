from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class BlosPageView(LoginRequiredMixin,TemplateView):
    template_name = 'blog/blog.html'
    login_url = '/auth/sign-in/'

class BlogDetailView(LoginRequiredMixin,TemplateView):
    template_name = 'blog/blog-details.html'
    login_url = '/auth/sign-in/'
