# scripts/create_pipeline.py
"""
Creates a complete Scikit-learn pipeline for the Titanic Survival Prediction project.
This pipeline bundles preprocessing, scaling, and model inference into a single artifact.
"""

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier  # Fallback if needed
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# --- Paths ---
DATA_PATH = "data/titanic_clean.csv"
MODEL_PATH = "models/sklearn_model.pkl"
PIPELINE_OUTPUT_PATH = "models/pipeline.pkl"

# --- Load dataset ---
df = pd.read_csv(DATA_PATH)
target_col = "survived"

X = df.drop(columns=[target_col])
y = df[target_col]

# --- Define categorical and numeric columns ---
categorical_cols = ["sex", "embarked", "class", "who", "embark_town", "alive"]
numeric_cols = ["pclass", "age", "sibsp", "parch", "fare", "adult_male", "alone"]

# --- Preprocessing ---
numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
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

# --- Load pretrained model (fallback to RandomForest if missing) ---
try:
    model = joblib.load(MODEL_PATH)
except Exception:
    print("⚠️ sklearn_model.pkl not found. Using RandomForestClassifier as fallback.")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(preprocessor.fit_transform(X), y)

# --- Create final pipeline ---
pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

# --- Fit pipeline to ensure compatibility ---
pipeline.fit(X, y)

# --- Save final pipeline ---
joblib.dump(pipeline, PIPELINE_OUTPUT_PATH)

print("✅ Pipeline successfully created and saved at:", PIPELINE_OUTPUT_PATH)
