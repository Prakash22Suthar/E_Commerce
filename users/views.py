from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UsersSerializers, UserLoginSerializer
from base.renderers import CustomRenderer
# Create your views here.


class UsersViewset(viewsets.ModelViewSet):
    """ 
    User CRUD with JWTAuthentication and CustomJsonResponse
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer]

class LoginAndTokenObtainView(TokenObtainPairView):
    """
    authenticate user with email and password and generate access_token, refresh_token
    """
    serializer_class = UserLoginSerializer