import torch
import numpy as np
import librosa
import torch.nn as nn

# Vocabulary
words = ['good','hello','morning','no','please','thank','yes','you']
idx_to_word = {i:w for i,w in enumerate(words)}

# Model
class SpeechModel(nn.Module):

    def __init__(self, input_size=13, hidden_size=64, num_classes=8):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        return out


model = SpeechModel()
model.load_state_dict(torch.load("speech_model.pth"))
model.eval()


def extract_feature(audio_path):

    audio, sr = librosa.load(audio_path, sr=16000)

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=13
    ).T

    max_len = 100

    if mfcc.shape[0] > max_len:
        mfcc = mfcc[:max_len]
    else:
        pad = max_len - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0,pad),(0,0)))

    return torch.tensor(mfcc, dtype=torch.float32).unsqueeze(0)


audio_file = "test.wav"   # change later

feature = extract_feature(audio_file)

with torch.no_grad():
    output = model(feature)
    prediction = torch.argmax(output).item()

print("Predicted word:", idx_to_word[prediction])