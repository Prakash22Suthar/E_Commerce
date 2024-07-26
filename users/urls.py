from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from .views import UsersViewset, LoginAndTokenObtainView

router = DefaultRouter()

router.register('', UsersViewset, basename="users")


urlpatterns = [
    path('users/', include(router.urls)),
    path('login/', LoginAndTokenObtainView.as_view(), name="login"),
    path('refresh-token/', TokenRefreshView.as_view(), name="refresh_token"),
    path('token-verify/', TokenVerifyView.as_view(), name="token_verify"),
]