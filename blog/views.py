from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Tag

# Create your views here.
class BlosPageView(LoginRequiredMixin,ListView):
    template_name = 'blog/blog.html'
    login_url = '/auth/sign-in/'
    model = Blog
    context_object_name = "blogs"
        

class BlogDetailView(LoginRequiredMixin,DetailView):
    template_name = 'blog/blog-details.html'
    login_url = '/auth/sign-in/'
    model = Blog
    context_object_name = "blog"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tags'] = data['blog'].tags.all()
        return data
