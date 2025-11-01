from fastapi import APIRouter, HTTPException

from app.models.predict import infer
from app.models.schemas import PredictInput, PredictOutput

router = APIRouter()


@router.post("/predict", response_model=PredictOutput)
def predict(payload: PredictInput):
    try:
        survived, probability = infer(payload)
        return PredictOutput(survived=survived, probability=probability)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")
