from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductViewset, CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()

router.register('products', ProductViewset , basename="products")
router.register('category', CategoryViewSet, basename="category")
router.register('sub-category', SubCategoryViewSet, basename="subcategory")

urlpatterns = [
    path('',include(router.urls)),
]