# scripts/predict_logic.py

import numpy as np
import joblib
from keras.models import load_model

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
    features = np.array([list(input_data.values())])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0][0]

    return {"survived": bool(round(prediction)), "confidence": float(prediction)}
