# prediction/urls.py

from django.urls import path
from .views import predict_view, form_view

urlpatterns = [
    path("predict/", predict_view, name="predict"),
    path("", form_view, name="form"),
]
