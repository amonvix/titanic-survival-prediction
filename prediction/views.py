# prediction/views.py
# pyright: reportMissingImports=false

import os
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from tensorflow.keras.models import load_model
from scripts.predict_logic import predict_survival




logger = logging.getLogger("prediction")

# Load model once
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.h5")
model = load_model(MODEL_PATH)
logger.info("✅ Keras model loaded successfully.")


def form_view(request):
    return render(request, "predict_form.html")


@csrf_exempt
def predict_view(request):
    logger.info(f"⚙️ Request method: {request.method}")
    logger.info(f"⚙️ Headers: {request.headers}")

    if request.method == "POST":
        try:
            input_data = json.loads(request.body)
            logger.info(f"Received input: {input_data}")

            result = predict_survival(input_data)
            logger.info(f"Prediction result: {result}")

            return JsonResponse(result, status=200)
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    else:
        from django.shortcuts import redirect
        return redirect("/")
    