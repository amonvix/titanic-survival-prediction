import os
import json
import numpy as np
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model

# Carregamento do modelo e scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, "../models/keras_model.keras"))
scaler = joblib.load(os.path.join(BASE_DIR, "../models/keras_scaler.pkl"))

category_mappings = {
    "sex": {"female": 0, "male": 1},
    "embarked": {"C": 0, "Q": 1, "S": 2},
    "class": {"First": 0, "Second": 1, "Third": 2},
    "who": {"child": 0, "man": 1, "woman": 2},
}

@csrf_exempt
def predict(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Mapeia strings para valores numéricos
            for key, mapping in category_mappings.items():
                if key in data:
                    data[key] = mapping[data[key]]

            input_data = np.array([list(data.values())])
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)
            survived = int(prediction[0][0] > 0.5)

            return JsonResponse({"prediction": survived})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)