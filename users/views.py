from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User
from .serializers import UsersSerializers, UserLoginSerializer
from base.throttles import CustomUserRateThrottle, CustomAnonRateThrottle
# Create your views here.


class UsersViewset(viewsets.ModelViewSet):
    """ 
    User CRUD with JWTAuthentication and CustomJsonResponse
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["email"] 
    # filter_backends = [OrderingFilter]
    # ordering_fields  = ["email"] 
    filter_backends = [OrderingFilter]
    ordering_fields = ["id"]

class LoginAndTokenObtainView(TokenObtainPairView):
    """
    authenticate user with email and password and generate access_token, refresh_token
    """
    serializer_class = UserLoginSerializer