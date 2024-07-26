from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrderViewset

router = DefaultRouter()

router.register('', OrderViewset, basename="orders")


urlpatterns = [
    path('orders/', include(router.urls)),
]