from django.urls import path

from core.api.auth_api import LoginAPI, RegisterAPI

app_name = "core"

urlpatterns = [
    path("auth/register/", RegisterAPI.as_view(), name="register_user"),
    path("auth/login/", LoginAPI.as_view(), name="login_user"),
]
