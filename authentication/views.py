from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm

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
    if request.user.is_authenticated:
        return redirect('core:home')  # agar foydalanuvchi login bo'lsa, home ga redirect

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('authentication:sign-in')
        else:
            messages.error(request, "Please correct the errors below.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()} maydonida - {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/auth.html', {'form': form, 'register': True})

