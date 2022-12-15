from django.urls import path

from core.api.auth_api import LoginAPI, ProfileAPI, RegisterAPI
from core.api.cart_api import (
    CartCheckoutAPI,
    GetUpdateDeleteCartItemAPI,
    ListCreateCartItemAPI,
)
from core.api.order_api import GetOrderAPI, ListOrderAPI
from core.api.payment_platform_api import (
    GetUpdateDeletePaymentPlatformAPI,
    ListCreatePaymentPlatformAPI,
)
from core.api.permission_api import ListUpdatePermissionAPI
from core.api.product_api import GetUpdateDeleteAPI, ListCreateAPI
from core.api.user_api import (
    ChangeStaffStatusAPI,
    GetUpdateDeleteUserAPI,
    ListCreateUserAPI,
)
from core.api.web_hooks_api import PaystackWebhookAPI

app_name = "core"

auth_urls = [
    path("auth/register/", RegisterAPI.as_view(), name="register_user"),
    path("auth/login/", LoginAPI.as_view(), name="login_user"),
    path("auth/profile/", ProfileAPI.as_view(), name="profile"),
]

product_urls = [
    path("products/", ListCreateAPI.as_view(), name="list_create_product"),
    path(
        "products/<uuid:id>/",
        GetUpdateDeleteAPI.as_view(),
        name="get_update_delete_product",
    ),
]

cart_urls = [
    path("cart/", ListCreateCartItemAPI.as_view(), name="list_create_cart"),
    path(
        "cart/<uuid:item_id>/",
        GetUpdateDeleteCartItemAPI.as_view(),
        name="get_update_delete_cart",
    ),
    path("cart/checkout/", CartCheckoutAPI.as_view(), name="checkout_cart"),
]

payment_platform_urls = [
    path(
        "payment-platforms/",
        ListCreatePaymentPlatformAPI.as_view(),
        name="list_create_payment_platform",
    ),
    path(
        "payment-platforms/<uuid:payment_platform_id>/",
        GetUpdateDeletePaymentPlatformAPI.as_view(),
        name="get_update_delete_payment_platform",
    ),
]

user_urls = [
    path("users/", ListCreateUserAPI.as_view(), name="list_create_users"),
    path(
        "users/<uuid:user_id>/",
        GetUpdateDeleteUserAPI.as_view(),
        name="get_update_delete_user",
    ),
    path(
        "users/<uuid:user_id>/change-staff-status/",
        ChangeStaffStatusAPI.as_view(),
        name="change_staff_status",
    ),
]

webhook_urls = [
    path("webhooks/paystack/", PaystackWebhookAPI.as_view(), name="paystack_webhook"),
]

order_urls = [
    path("orders/", ListOrderAPI.as_view(), name="list_order"),
    path("orders/<uuid:order_id>/", GetOrderAPI.as_view(), name="get_order"),
]

permission_urls = [
    path(
        "permission/", ListUpdatePermissionAPI.as_view(), name="list_update_permission"
    ),
]

urlpatterns = [
    *auth_urls,
    *product_urls,
    *cart_urls,
    *payment_platform_urls,
    *webhook_urls,
    *order_urls,
    *user_urls,
    *permission_urls,
]
