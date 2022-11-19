from django.urls import path

from core.api.auth_api import LoginAPI, RegisterAPI
from core.api.cart_api import GetUpdateDeleteCartItemAPI, ListCreateCartItemAPI
from core.api.product_api import GetUpdateDeleteAPI, ListCreateAPI

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

urlpatterns = [
    *auth_urls,
    *product_urls,
    *cart_urls,
]
