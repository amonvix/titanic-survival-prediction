from fastapi import FastAPI

from app.routers import predict

app = FastAPI(title="Titanic API")

app.include_router(predict.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "API do Titanic em execução!"}


@app.get("/health")
def health():
    return {"status": "healthy"}
