from fastapi import FastAPI

from app.routers.predict import router as predict_router

app = FastAPI()

app.include_router(predict_router, prefix="/predict", tags=["predict"])


@app.get("/")
def root():
    return {"status": "ok", "message": "API do Titanic em execução!"}


@app.get("/health")
def health():
    return {"status": "healthy"}
