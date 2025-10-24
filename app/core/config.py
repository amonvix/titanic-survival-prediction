import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "titanic-api")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/models/titanic_model.joblib")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
