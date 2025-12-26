from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import mixins, viewsets, permissions, status

from authentication.models import CustomUser
from .serializers import CustomTokenObtainSerializer
from authentication.serializers import CustomUserSerializer

# Create your views here.

# Permissions

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    
class RegisterUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user) and not (request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class UserRegister(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
class AdminUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

class CustomPermisson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
        
        
        
# Views
class HomePageView(APIView):
    permission_classes = [permissions.IsAuthenticated, CustomPermisson]
    
    def get(self, request):
        return Response(
            {"message": "Hello world!"},
            status=status.HTTP_200_OK,
        )

        
