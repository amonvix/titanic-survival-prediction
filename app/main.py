from fastapi import FastAPI, HTTPException

from app.core.config import settings
from app.models.predict import infer
from app.models.schemas import PredictInput, PredictOutput

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "API do Titanic em execução!",
        "app": settings.APP_NAME,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictOutput)
def predict(payload: PredictInput):
    try:
        survived, probability = infer(payload)
        return PredictOutput(survived=survived, probability=probability)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500, detail="Modelo não encontrado. Configure MODEL_PATH."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha na predição: {e}")
