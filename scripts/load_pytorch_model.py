import joblib
import pandas as pd
import torch
from torch import nn


# --- Define novamente a arquitetura (mesma usada no treino) ---
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


# --- Recria o modelo e carrega os pesos ---
model = TitanicModel(input_dim=13)  # o número deve bater com o treino
model.load_state_dict(torch.load("models/pytorch_model.pt", map_location="cpu"))
model.eval()

# --- Carrega o scaler ---
scaler = joblib.load("models/pytorch_scaler.pkl")

# --- Cria um exemplo de entrada ---
df = pd.read_csv("data/titanic_clean.csv")  # caminho relativo
sample_data = df.drop(columns=["survived"]).iloc[[0]].to_numpy()  # exemplo de features

# --- Scale and convert to tensor ---
scaled_data = scaler.transform(sample_data)
input_tensor: torch.Tensor = torch.tensor(scaled_data, dtype=torch.float32)

# --- Faz a predição ---
with torch.no_grad():
    output = model(input_tensor)
    prediction = (output >= 0.5).int().item()

print(f"🔍 Model raw output: {output.item():.4f}")
print(
    f"🧠 Predicted survival: {'✅ Survived' if prediction == 1 else '❌ Did not survive'}"
)
