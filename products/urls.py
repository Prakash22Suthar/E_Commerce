from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProductViewset

router = DefaultRouter()

router.register('', ProductViewset , basename="products")

urlpatterns = [
    path('products/',include(router.urls)),
]