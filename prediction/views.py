# Caminho: prediction/views.py

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from scripts.predict_logic import predict_survival


@csrf_exempt
def predict_view(request):
    """
    Django view para predição de sobrevivência no Titanic.
    Espera um JSON via POST com os dados necessários.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Use POST method"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        prediction_result = predict_survival(data)
        return JsonResponse({"prediction": prediction_result}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def health_check(request):
    return JsonResponse({"status": "ok", "message": "Titanic API running!"})
