# scripts/create_pipeline.py

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = "data/titanic_clean.csv"
PIPELINE_OUTPUT_PATH = "models/pipeline.pkl"

df = pd.read_csv(DATA_PATH)
X = df.drop(columns=["survived"])
y = df["survived"]

categorical_cols = ["sex", "embarked"]
numeric_cols = ["pclass", "age", "sibsp", "parch", "fare"]

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols),
    ]
)

model = RandomForestClassifier(n_estimators=200, random_state=42)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)

pipeline.fit(X, y)

joblib.dump(pipeline, PIPELINE_OUTPUT_PATH)

print("✅ Pipeline salvo em:", PIPELINE_OUTPUT_PATH)
