# scripts/predict_logic.py

import numpy as np
import joblib
from keras.models import load_model

category_mappings = {
    "sex": {"female": 0, "male": 1},
    "embarked": {"C": 0, "Q": 1, "S": 2},
    "class": {"First": 0, "Second": 1, "Third": 2},
    "who": {"child": 0, "man": 1, "woman": 2},
    "embark_town": {"Cherbourg": 0, "Queenstown": 1, "Southampton": 2},
    "alive": {"no": 0, "yes": 1},
}


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


# Load model and scaler once (lazy init possible later)
MODEL_PATH = "models/keras_model.keras"
SCALER_PATH = "models/keras_scaler.pkl"

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_survival(input_data: dict) -> dict:
    """
    Predicts survival using the trained Keras model.
    :param input_data: dict with input features
    :return: dict with prediction result
    """
    input_data = preprocess_input(input_data)
    features = np.array([list(input_data.values())])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0][0]

    return {"survived": bool(round(prediction)), "confidence": float(prediction)}
