from django.urls import path

from core.api.auth_api import LoginAPI, RegisterAPI
from core.api.cart_api import GetUpdateDeleteCartItemAPI, ListCreateCartItemAPI
from core.api.product_api import GetUpdateDeleteAPI, ListCreateAPI
from core.api.payment_platform_api import (
    ListCreatePaymentPlatformAPI,
    GetUpdateDeletePaymentPlatformAPI,
)
from core.api.web_hooks_api import PaystackWebhookAPI


app_name = "core"

auth_urls = [
    path("auth/register/", RegisterAPI.as_view(), name="register_user"),
    path("auth/login/", LoginAPI.as_view(), name="login_user"),
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

webhook_urls = [
    path("webhooks/paystack/", PaystackWebhookAPI.as_view(), name="paystack_webhook"),
]

urlpatterns = [
    *auth_urls,
    *product_urls,
    *cart_urls,
    *payment_platform_urls,
    *webhook_urls,
]
