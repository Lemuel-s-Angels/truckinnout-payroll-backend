from django.shortcuts import render
from rest_framework import permissions, viewsets

from users.models import CustomUser
from users.serializers import CustomUserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
