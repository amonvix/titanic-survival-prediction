# Caminho: prediction/urls.py

from django.urls import path

from .views import health_check, predict_view

urlpatterns = [
    path("", health_check, name="health_check"),
    path("predict/", predict_view, name="predict"),
]
