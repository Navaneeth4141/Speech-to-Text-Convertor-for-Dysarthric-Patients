import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("training_dataset.csv")

# -----------------------------
# Create vocabulary
# -----------------------------
words = sorted(df["transcript"].unique())
word_to_idx = {w: i for i, w in enumerate(words)}

print("Vocabulary:", word_to_idx)

# -----------------------------
# Dataset Class
# -----------------------------
class SpeechDataset(Dataset):

    def __init__(self, dataframe):
        self.df = dataframe

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        feature_path = self.df.iloc[idx]["feature_path"]
        transcript = self.df.iloc[idx]["transcript"]

        feature = np.load(feature_path)

        # ---- FIX VARIABLE LENGTH AUDIO ----
        max_len = 100

        if feature.shape[0] > max_len:
            feature = feature[:max_len]
        else:
            pad_size = max_len - feature.shape[0]
            feature = np.pad(feature, ((0, pad_size), (0, 0)), mode="constant")

        feature = torch.tensor(feature, dtype=torch.float32)

        label = word_to_idx[transcript]
        label = torch.tensor(label)

        return feature, label


# -----------------------------
# Create Dataset + DataLoader
# -----------------------------
dataset = SpeechDataset(df)

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True
)

# -----------------------------
# Define Model
# -----------------------------
class SpeechModel(nn.Module):

    def __init__(self, input_size=13, hidden_size=64, num_classes=8):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):

        out, _ = self.lstm(x)

        out = out[:, -1, :]

        out = self.fc(out)

        return out


model = SpeechModel()

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# -----------------------------
# Training Loop
# -----------------------------
epochs = 10

for epoch in range(epochs):

    total_loss = 0

    for x, y in loader:

        optimizer.zero_grad()

        outputs = model(x)

        loss = criterion(outputs, y)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}  Loss: {total_loss:.4f}")

# -----------------------------
# Save Model
# -----------------------------
torch.save(model.state_dict(), "speech_model.pth")

print("Model training completed successfully.")