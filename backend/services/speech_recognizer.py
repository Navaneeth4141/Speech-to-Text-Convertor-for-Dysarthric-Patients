import torch
import numpy as np
import librosa
import torch.nn as nn
import os
import subprocess
import tempfile


# Vocabulary
words = ['good','hello','morning','no','please','thank','yes','you']
idx_to_word = {i:w for i,w in enumerate(words)}


# Deep Learning Model
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


# Load trained model
model = SpeechModel()

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "scripts",
    "speech_model.pth"
)

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))

model.eval()


def convert_to_wav(input_path):

    temp_wav = tempfile.mktemp(suffix=".wav")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        temp_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return temp_wav


def extract_features(audio_path):

    wav_path = convert_to_wav(audio_path)

    audio, sr = librosa.load(wav_path, sr=16000)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13).T

    max_len = 100

    if mfcc.shape[0] > max_len:
        mfcc = mfcc[:max_len]
    else:
        pad = max_len - mfcc.shape[0]
        mfcc = np.pad(mfcc, ((0,pad),(0,0)))

    return torch.tensor(mfcc, dtype=torch.float32).unsqueeze(0)


def predict(audio_path):

    feature = extract_features(audio_path)

    with torch.no_grad():

        output = model(feature)

        prediction = torch.argmax(output).item()

    return idx_to_word[prediction]