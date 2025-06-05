# prediction/urls.py

from django.urls import path
from .views import PredictView, form_view


urlpatterns = [
    path("", form_view),  # / → mostra formulário
    path("predict/", PredictView.as_view(), name="predict"),
]
