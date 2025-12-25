from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class HomePageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(
            {"message": "Hello world!"},
            status=status.HTTP_200_OK,
        )