from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser

# Create your views here.

def signin_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = CustomUser.objects.filter(username=username).first()
        if not user:
            messages.info(request, "User not found")
        if not user.password == password:
            messages.info(request, "Password is incorrect")
        login(request, user)
        
        return redirect("home")
        
    return render(request, "authentication/auth.html")

def logout_view(request):
    logout(request)
    return render(request, "authentication/auth.html")

def signup_view(request):
    return render(request, 'authentication/auth.html')

