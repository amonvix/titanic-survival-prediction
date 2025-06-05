# titanic_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/predict/', permanent=False)),  # redireciona /
    path('admin/', admin.site.urls),
    path('', include('prediction.urls')),
]
