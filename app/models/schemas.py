from pydantic import BaseModel, Field


class PredictInput(BaseModel):
    pclass: int = Field(..., ge=1, le=3)
    sex: str
    age: float
    sibsp: int
    parch: int
    fare: float
    embarked: str


class PredictOutput(BaseModel):
    survived: int
    probability: float
