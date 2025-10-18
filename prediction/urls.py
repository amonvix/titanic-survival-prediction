from django.urls import path

from .views import health_check, predict

urlpatterns = [
    path("", health_check),
    path("predict/", predict),
]
