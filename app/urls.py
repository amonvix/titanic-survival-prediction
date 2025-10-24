# app/urls.py
from .views import health_check
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("prediction.urls")),
    path('health', health_check, name='health_check'),
    path("admin/", admin.site.urls),
]
