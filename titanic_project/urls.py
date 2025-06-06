# titanic_project/urls.py

from django.contrib import admin
from django.urls import path
from prediction.views import PredictView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "predict/", PredictView.as_view()
    ),  # está apontando pra predict() que não existe no views.py
]
