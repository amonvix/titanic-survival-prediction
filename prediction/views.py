from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def health_check(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
def predict(request):
    return JsonResponse(
        {"message": "Prediction endpoint placeholder (model disabled for CI tests)"}
    )
