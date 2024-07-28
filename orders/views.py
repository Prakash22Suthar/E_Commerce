from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db import transaction

from users.models import User
from products.models import Product
from .models import Orders, Orderitem
from .serializers import OrderSerializer, OrderListSerializer,OrderCreateUpdateSerializer
from .utils import generate_orderid

from base.renderers import CustomRenderer
# Create your views here.


class OrderViewset(viewsets.ModelViewSet):
    """Viewset for CURD of Order"""
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer]

    def get_serializer_class(self):
        actions = {
            "list":OrderListSerializer,
            "create":OrderCreateUpdateSerializer,
            "update":OrderCreateUpdateSerializer
        }
        if self.action in actions:
            self.serializer_class = actions.get(self.action)
        return super().get_serializer_class()

    def get_queryset(self):
        username = self.request.GET.get("username", None)
        if username is not None:
            queryset = self.queryset.filter(created_by__username=username)
        else:
            queryset = self.queryset
        return queryset
    
    def create(self, request, *args, **kwargs):
        order_item_data = request.data.pop("order_items", None)
        serializer = self.get_serializer(data=request.data, context={"order_items":order_item_data})    
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, *args, **kwargs):
        instance = Orders.objects.get(id=kwargs.get("pk"))
        order_item_data = request.data.pop("order_items", None)
        serializer = self.get_serializer(instance, data=request.data, context={"order_items":order_item_data})    
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
