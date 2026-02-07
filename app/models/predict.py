# app/models/predict.py

import joblib
import pandas as pd
from pathlib import Path

PIPELINE_PATH = Path("models/pipeline.pkl")

_pipeline = None

def _load_pipeline():
    global _pipeline
    if _pipeline is None:
        if not PIPELINE_PATH.exists():
            raise FileNotFoundError("models/pipeline.pkl not found")
        _pipeline = joblib.load(PIPELINE_PATH)
    return _pipeline

def infer(payload):
    pipeline = _load_pipeline()

    data = pd.DataFrame([payload.model_dump()])

    proba = pipeline.predict_proba(data)[0][1]
    survived = int(proba >= 0.5)

    return survived, float(proba)
