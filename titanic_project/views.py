import os, json, traceback, joblib
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model

# Carregamento do modelo e scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

category_mappings = {
    "sex": {"female": 0, "male": 1},
    "embarked": {"C": 0, "Q": 1, "S": 2},
    "class": {"First": 0, "Second": 1, "Third": 2},
    "who": {"child": 0, "man": 1, "woman": 2},
    "deck": {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "Unknown": 7},
    # "embark_town": {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2}  # exemplo
}

def load_prediction_components():
    model = load_model("models/keras_model.keras")
    scaler = joblib.load("models/keras_scaler.pkl")
    return model, scaler

@csrf_exempt
def predict(request):
    if request.method == "POST":
        try:
            model, scaler = load_prediction_components()
            data = json.loads(request.body)

            warnings = []

            # Converte strings para formato padronizado e faz o mapeamento
            for key, mapping in category_mappings.items():
                if key not in data:
                    warnings.append(f"[⚠️] Chave '{key}' esperada no JSON mas não encontrada.")
                    continue

            raw_value = str(data[key]).strip()
            if raw_value not in mapping:
                return JsonResponse({
                "error": f"Valor '{raw_value}' da chave '{key}' não está no mapeamento válido: {list(mapping.keys())}"
                }, status=400)

            data[key] = mapping[raw_value]

            input_data = np.array([list(data.values())])
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)
            confidence = float(prediction[0][0])
            survived = bool(confidence > 0.5)

            response = {
                "survived": survived,
                "confidence": round(confidence, 4)
            }
            if warnings:
                response["warnings"] = warnings

            return JsonResponse(response)

        except Exception as e:
            import traceback
            return JsonResponse({"error": str(e), "trace": traceback.format_exc()}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)

