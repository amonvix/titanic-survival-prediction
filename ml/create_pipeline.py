# scripts/create_pipeline.py
"""
Creates a complete Scikit-learn pipeline for the Titanic Survival Prediction project.
This pipeline bundles preprocessing, scaling, and model inference into a single artifact.
"""

import joblib
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier  # Fallback if needed
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# --- Paths ---
DATA_PATH = "data/titanic_clean.csv"
PIPELINE_OUTPUT_PATH = "models/pipeline.pkl"

Path("models").mkdir(parents=True, exist_ok=True)

# --- Load dataset ---
df = pd.read_csv(DATA_PATH)
target_col = "survived"

FEATURES = [
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "fare",
    "embarked",
]

X = df[FEATURES]
y = df[target_col]

# --- Define categorical and numeric columns ---
categorical_cols = ["sex", "embarked"]
numeric_cols = ["pclass", "age", "sibsp", "parch", "fare"]

# --- Preprocessing ---
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

# --- Model ---
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
)

# --- Final pipeline ---
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)

# --- Train pipeline ---
pipeline.fit(X, y)

# --- Save pipeline ---
joblib.dump(pipeline, PIPELINE_OUTPUT_PATH)

print("✅ Production pipeline created and saved at:", PIPELINE_OUTPUT_PATH)