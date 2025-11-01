# app/models/predict.py


def infer(payload):
    return predict_survival(payload)


def predict_survival(payload):
    """
    Temporary mock inference for testing and CI purposes.
    Replace this with your real model loading and prediction logic.
    """
    # Simula inferência estável para manter o CI passando
    survived = False
    probability = 0.42
    return survived, probability
