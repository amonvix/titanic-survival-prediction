# scripts/predict_logic.py
"""
Predict logic using the full sklearn pipeline (preprocessing + scaler + model).
This assumes models/pipeline.pkl exists and was built using create_pipeline.py.
"""

from pathlib import Path

import joblib
import pandas as pd

# Path to the complete pipeline
PIPELINE_PATH = Path("models/pipeline.pkl")

# Load pipeline lazily (once on module import)
pipeline = joblib.load(PIPELINE_PATH)


def predict_survival(input_data: dict) -> dict:
    """
    Takes input_data as a dict matching the raw Titanic features.
    Example:
        {
            "pclass": 2,
            "sex": "male",
            "age": 29,
            "sibsp": 1,
            "parch": 0,
            "fare": 32.5,
            "embarked": "S",
            "class": "Second",
            "who": "man",
            "adult_male": 1,
            "embark_town": "Southampton",
            "alone": 1
        }
    """
    # ✅ Convert dict to DataFrame with a single row
    X = pd.DataFrame([input_data])

    # ✅ Predict class and probability
    prediction_proba = pipeline.predict_proba(X)[0][1]  # probabilidade de sobreviver
    prediction_class = pipeline.predict(X)[0]  # classe final

    return {"survived": bool(prediction_class), "confidence": float(prediction_proba)}
