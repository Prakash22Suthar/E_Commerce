from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer
from .models import Product, Category, Subcategory
# Create your views here.

def get_category_data(category_data:dict, sub_category_data:dict):
    category, create = Category.objects.get_or_create(**category_data)
    # import ipdb
    # ipdb.set_trace()
    sub_category_data["category"] = category
    sub_category ,create = Subcategory.objects.get_or_create(**sub_category_data)
    return category.id, sub_category.id

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        category_data = request.data.pop("category")
        sub_category_data = request.data.pop("subcategory")
        category, subcategory = get_category_data(category_data, sub_category_data)
        request.data["category"] = category
        request.data["subcategory"] = subcategory
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        request.data["category"] = request.data.get("category",instance.category.id)
        request.data["subcategory"] = request.data.get("subcategory",instance.subcategory.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
