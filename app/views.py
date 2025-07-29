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
    "embark_town": {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2},
    "pclass": {1: 0, 2: 1, 3: 2}, # Manter se pclass for categórico
    "sibsp": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 8: 6} # Manter se sibsp for categórico
}

# Define the expected feature order (deve ser consistente com o treinamento do modelo)
FEATURE_ORDER = [
    "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked",
    "class", "who", "adult_male", "deck", "embark_town", "alone"
]

# Variáveis globais para o modelo e scaler
MODEL = None
SCALER = None

def load_prediction_components():
    """Carrega o modelo Keras e o scaler Joblib."""
    global MODEL, SCALER
    if MODEL is None or SCALER is None:
        try:
            model_path = os.path.join(BASE_DIR, "../models/keras_model.keras")
            scaler_path = os.path.join(BASE_DIR, "../models/keras_scaler.pkl")
            MODEL = load_model(model_path)
            SCALER = joblib.load(scaler_path)
            print("Modelo e scaler carregados com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar o modelo ou scaler: {e}")
            MODEL = None
            SCALER = None
    return MODEL, SCALER

# Carrega os componentes quando o módulo é importado
load_prediction_components()

@csrf_exempt
def predict(request):
    if request.method == "POST":
        scaler = load_prediction_components()

        if scaler is None:
            return JsonResponse({"error": "Scaler not loaded. Please check server logs."}, status=500)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error parsing request body: {e}"}, status=400)

        input_features = []
        for feature in FEATURE_ORDER:
            value = data.get(feature)

            if value is None:
                return JsonResponse({"error": f"Missing required feature: '{feature}' in input data."}, status=400)

            # Aplica o mapeamento de categoria, se aplicável
            if feature in category_mappings:
                # Tenta mapear o valor. Se não encontrar, retorna erro ou um valor padrão para "desconhecido"
                mapped_value = category_mappings[feature].get(value)
                if mapped_value is None:
                    # Se o valor categórico não for encontrado no mapeamento
                    # e não for um valor que você espera tratar como numérico depois,
                    # deve-se retornar um erro ou um valor "desconhecido" adequado.
                    return JsonResponse({"error": f"Invalid value '{value}' for category '{feature}'. Value not in mapping."}, status=400)
                input_features.append(mapped_value)
            else:
                # Para features numéricas, tenta converter para float.
                # Isso inclui 'age', 'fare', 'parch', 'adult_male', 'alone'
                try:
                    # Tenta converter para float (para 'age', 'fare') ou int (para outros numéricos binários/contagens)
                    if isinstance(value, (int, float)):
                        input_features.append(float(value)) # Converte tudo para float para consistência com o scaler
                    elif isinstance(value, str):
                        # Trata strings que deveriam ser numéricas (ex: "25.0")
                        input_features.append(float(value))
                    else:
                        # Se o valor não for numérico e não for uma string convertível
                        return JsonResponse({"error": f"Invalid data type for numeric feature '{feature}': expected numeric, got '{type(value).__name__}'."}, status=400)
                except (ValueError, TypeError):
                    return JsonResponse({"error": f"Could not convert value '{value}' to numeric for feature '{feature}'."}, status=400)

        try:
            input_data = np.array([input_features])
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)
            survived = bool(prediction[0][0] > 0.5)
            confidence = float(prediction[0][0])

            return JsonResponse({
                "survived": survived,
                "confidence": confidence,
                "message": "Prediction successful"
            })

        except Exception as e:
            return JsonResponse({"error": f"Prediction failed due to internal processing error: {e}"}, status=500)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)