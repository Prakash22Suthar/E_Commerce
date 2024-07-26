from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db import transaction

from users.models import User
from products.models import Product
from .models import Orders, Orderitem
from .serializers import OrderSerializer
from .utils import generate_orderid

from base.renderers import CustomRenderer
# Create your views here.


class OrderViewset(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer]

    def get_queryset(self):
        username = self.request.GET.get("username", self.request.user.username)
        if username is not None:
            queryset = self.queryset.filter(order_created_by__username=username)
        else:
            queryset = self.queryset
        return queryset

    def create(self, request, *args, **kwargs):
        request.data["order_id"]= generate_orderid()
        user = User.objects.get(id=request.data.get("order_by"))
        quantity = request.data.pop("quantity", 0)
        product_ids = request.data.pop("product",None)
        request.data["user"] = user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        products: Product = Product.objects.filter(id__in=product_ids)

        order_item_data = [
            Orderitem(
            order = order,
            quantity =quantity,
            amount = float(quantity * product.price),
            items = product
            ) for product in products
        ]
        Orderitem.objects.bulk_create(order_item_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)