# scripts/save_sklearn_model.py

import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load and preprocess data
df = pd.read_csv("data/titanic_clean.csv")
X = df.drop(columns=["survived"]).values
y = df["survived"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, _, y_train, _ = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump(model, "models/sklearn_model.pkl")
joblib.dump(scaler, "models/sklearn_scaler.pkl")

print("✅ Scikit-learn model and scaler saved successfully.")
