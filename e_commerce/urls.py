"""e_commerce URL Configuration
"""
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("core.urls")),
]
