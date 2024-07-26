from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include("users.urls")),
    path('api/',include("orders.urls")),
    path('api/',include("products.urls")),

    path('auth/', include("rest_framework.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
