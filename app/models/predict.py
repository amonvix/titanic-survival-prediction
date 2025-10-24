from pathlib import Path

import joblib
import pandas as pd

from app.core.config import settings

# Carregamos modelo uma única vez
model = None
model_path = Path(settings.MODEL_PATH)

if model_path.exists():
    model = joblib.load(model_path)
else:
    model = None  # Se não achado, tratamos no infer()


def transform_input(payload_dict):
    """Converte as 7 features originais da API nas 13 features esperadas pelo pipeline."""
    p = payload_dict.copy()

    # 1. class derivada de pclass (ajuste de rótulos conforme dataset original)
    p["class"] = {1: "First", 2: "Second", 3: "Third"}[p["pclass"]]

    # 2. who: man, woman ou child
    p["who"] = "child" if p["age"] < 16 else "man" if p["sex"] == "male" else "woman"

    # 3. adult_male: boolean se adulto e masculino
    p["adult_male"] = p["age"] >= 16 and p["sex"] == "male"

    # 4. embark_town: conversão de código para nome completo
    p["embark_town"] = {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}[
        p["embarked"]
    ]

    # 5. alone: se sibsp == 0 e parch == 0
    p["alone"] = (p["sibsp"] + p["parch"]) == 0

    # 6. alive: placeholder para o modelo (será ignorado, era target no dataset)
    p["alive"] = "yes"

    return p


def infer(payload):
    """Recebe o Pydantic payload, transforma, envia ao modelo e retorna (survived, probability)."""
    if model is None:
        raise FileNotFoundError(f"Modelo não encontrado em {model_path}")

    # Converter entrada crua -> formato esperado pelo modelo
    transformed = transform_input(payload.dict())

    df = pd.DataFrame([transformed])

    # Predição
    prediction = model.predict(df)[0]

    # Probabilidade (se disponível no pipeline)
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(df)[0][1])
    else:
        probability = 1.0 if prediction == 1 else 0.0

    return int(prediction), probability
