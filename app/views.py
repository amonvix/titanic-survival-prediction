import json
import os

import joblib
import numpy as np
import numpy.typing as npt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Base dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Category mappings
category_mappings = {
    "sex": {"female": 0, "male": 1},
    "embarked": {"C": 0, "Q": 1, "S": 2},
    "class": {"First": 0, "Second": 1, "Third": 2},
    "who": {"child": 0, "man": 1, "woman": 2},
    "deck": {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "Unknown": 7},
    "embark_town": {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2},
    "pclass": {1: 0, 2: 1, 3: 2},
    "sibsp": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 8: 6},
}

# Expected input order
FEATURE_ORDER = [
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "fare",
    "embarked",
    "class",
    "who",
    "adult_male",
    "deck",
    "embark_town",
    "alone",
]

MODEL = None
SCALER = None


def load_prediction_components():
    """Load sklearn model and scaler."""
    global MODEL, SCALER

    if MODEL is None or SCALER is None:
        model_path = os.path.join(BASE_DIR, "../models/sklearn_model.pkl")
        scaler_path = os.path.join(BASE_DIR, "../models/sklearn_scaler.pkl")

        MODEL = joblib.load(model_path)
        SCALER = joblib.load(scaler_path)

    return MODEL, SCALER


def health_check(request):
    """Simple health check."""
    return JsonResponse({"status": "ok"})


@csrf_exempt
def predict(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    model, scaler = load_prediction_components()

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    input_features = []
    for feature in FEATURE_ORDER:
        value = data.get(feature)

        if value is None:
            return JsonResponse(
                {"error": f"Missing required feature: '{feature}'"}, status=400
            )

        if feature in category_mappings:
            mapped_value = category_mappings[feature].get(value)
            if mapped_value is None:
                return JsonResponse(
                    {
                        "error": f"Invalid value '{value}' for category '{feature}'. Value not in mapping."
                    },
                    status=400,
                )
            input_features.append(mapped_value)
        else:
            try:
                input_features.append(float(value))
            except (ValueError, TypeError):
                return JsonResponse(
                    {
                        "error": f"Could not convert '{value}' to numeric for feature '{feature}'."
                    },
                    status=400,
                )

    try:
        input_data: npt.NDArray[np.float32] = np.array(
            [input_features], dtype=np.float32
        )
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        survived = bool(prediction[0] > 0.5)
        confidence = float(prediction[0])

        return JsonResponse(
            {
                "survived": survived,
                "confidence": confidence,
                "message": "Prediction successful",
            }
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Prediction failed: {e}"},
            status=500,
        )
