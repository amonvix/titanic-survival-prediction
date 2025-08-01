# scripts/predict_logic.py
import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Category encoding map
category_mappings = {
    "sex": {"female": 0, "male": 1},
    "embarked": {"C": 0, "Q": 1, "S": 2},
    "class": {"First": 0, "Second": 1, "Third": 2},
    "who": {"child": 0, "man": 1, "woman": 2},
    "deck": {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "Unknown": 7},
    "embark_town": {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2},
    "alive": {"no": 0, "yes": 1},
}

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALER_PATH = os.path.join(BASE_DIR, "models", "keras_scaler.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.h5")

# Lazy-loaded scaler
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def preprocess_input(raw_data: dict) -> dict:
    processed = {}
    for key, value in raw_data.items():
        if key in category_mappings:
            try:
                processed[key] = category_mappings[key][value]
            except KeyError:
                raise ValueError(f"Invalid value '{value}' for field '{key}'")
        else:
            processed[key] = value
    return processed


def predict_survival(input_data: dict) -> dict:
    input_data = preprocess_input(input_data)
    features = np.array([list(input_data.values())])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0][0]

    return {"survived": bool(round(prediction)), "confidence": float(prediction)}
