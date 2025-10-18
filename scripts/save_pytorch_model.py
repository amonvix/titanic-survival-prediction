import os

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Create output folder
os.makedirs("models", exist_ok=True)

# Load and preprocess data
df = pd.read_csv("data/titanic_clean.csv")
X = df.drop(columns=["survived"]).values
y = df["survived"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, _, y_train, _ = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(np.array(y_train).reshape(-1, 1), dtype=torch.float32)


# Define PyTorch model
class TitanicModel(nn.Module):
    def __init__(self, input_dim):
        super(TitanicModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)


model = TitanicModel(input_dim=X_train_tensor.shape[1])
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train
for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

# Save model and scaler
torch.save(model.state_dict(), "models/pytorch_model.pt")
joblib.dump(scaler, "models/pytorch_scaler.pkl")

print("✅ PyTorch model and scaler saved successfully.")
