from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer, ProductListSerializer, CategorySerializer, SubcategorySerializer
from .models import Product, Category, Subcategory
from base.renderers import CustomRenderer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    """Viewset for CURD of Product Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [CustomRenderer]

class SubCategoryViewSet(viewsets.ModelViewSet):
    """Viewset for CURD of Product Sub Category"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    renderer_classes = [CustomRenderer]

class ProductViewset(viewsets.ModelViewSet):
    """Viewset for CURD of Product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [CustomRenderer]

    def get_serializer_class(self):
        actions = {
            "list":ProductListSerializer,
            "create":ProductSerializer,
            "update":ProductSerializer,
        }
        if self.action in actions:
            self.serializer_class = actions.get(self.action)

        return super().get_serializer_class()
