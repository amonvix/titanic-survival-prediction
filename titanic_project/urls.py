# titanic_project/urls.py

from django.contrib import admin
from django.urls import path
from titanic_project.views import status

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", status),
]
