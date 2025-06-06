import os
import json
import numpy as np
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model

# Base dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Category mappings
category_mappings = {
    "sex": {"female": 0, "male": 1},
    "embarked": {"C": 0, "Q": 1, "S": 2},
    "class": {"First": 0, "Second": 1, "Third": 2},
    "who": {"child": 0, "man": 1, "woman": 2},
    "deck": {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "Unknown": 7},
    "embark_town": {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2}
}

# Load model and scaler
def load_prediction_components():
    model = load_model(os.path.join(BASE_DIR, "../models/keras_model.keras"))
    scaler = joblib.load(os.path.join(BASE_DIR, "../models/keras_scaler.pkl"))
    return model, scaler

@csrf_exempt
def predict(request):
    if request.method == "POST":
        try:
            model, scaler = load_prediction_components()
            data = json.loads(request.body)

            # Encode string values
            for key, mapping in category_mappings.items():
                if key in data:
                    data[key] = mapping.get(data[key], -1)  # default to -1 if not found

            input_data = np.array([list(data.values())])
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)
            survived = bool(prediction[0][0] > 0.5)
            confidence = float(prediction[0][0])

            return JsonResponse({
                "survived": survived,
                "confidence": confidence
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)
