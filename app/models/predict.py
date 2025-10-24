from typing import Tuple

import joblib
import numpy as np

from app.core.config import settings

from .schemas import PredictInput

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(settings.MODEL_PATH)
    return _model


def infer(payload: PredictInput) -> Tuple[int, float]:
    model = load_model()
    X = np.array(
        [
            [
                payload.pclass,
                1 if payload.sex.lower() == "male" else 0,
                payload.age,
                payload.sibsp,
                payload.parch,
                payload.fare,
                {"C": 0, "Q": 1, "S": 2}.get(payload.embarked.upper(), 2),
            ]
        ],
        dtype=float,
    )
    proba = float(model.predict_proba(X)[0, 1])
    return int(proba >= 0.5), proba
