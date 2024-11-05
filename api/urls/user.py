# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )
# from rest_framework import routers

# from ..views.user import CustomTokenObtainPairView, CustomerAPI, CustomerloginViewSet,CustomerloginCheckView

# router = routers.DefaultRouter()

# router.register("customer", CustomerAPI)
# router.register(r'customerlogins', CustomerloginViewSet)

# urlpatterns = [
#     path("login/", CustomTokenObtainPairView.as_view(), name="login"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path('check-customerlogin/', CustomerloginCheckView.as_view(), name='check_customerlogin'),
# ] + router.urls

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers

from ..views.user import CustomTokenObtainPairView, CustomerAPI, CustomerloginViewSet,CustomerloginCheckView, CustomerNormalLoginCreateView, CustomerLoginAPIView, SetNullPasswordView,PasswordResetRequestView,PasswordResetConfirmView, CreateGuestCustomerView


router = routers.DefaultRouter()

router.register("customer", CustomerAPI)
router.register(r'customerlogins', CustomerloginViewSet)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('check-customerlogin/', CustomerloginCheckView.as_view(), name='check_customerlogin'),
    path('customer-normal-login/', CustomerLoginAPIView.as_view(), name='customer-normal-login'),
    path('customer-normal-register/', CustomerNormalLoginCreateView.as_view(), name='register'),
    path('change-null-pw/', SetNullPasswordView.as_view(), name='set_null_password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    # path('password-reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm_api'),
    path('password-reset/confirm/<str:reset_token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('create-guest/', CreateGuestCustomerView.as_view(), name='create-guest'),

] + router.urls

