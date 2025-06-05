import pandas as pd
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# Create directory if needed
os.makedirs("models", exist_ok=True)

# Load and scale data
df = pd.read_csv("data/titanic_clean.csv")
X = df.drop(columns=["survived"]).values
y = df["survived"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, _, y_train, _ = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train
model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)

# Save model and scaler
model.save("models/keras_model.keras")
joblib.dump(scaler, "models/keras_scaler.pkl")

print("✅ Keras model and scaler saved successfully.")
