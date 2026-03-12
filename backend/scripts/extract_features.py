import os
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm

BASE_DATA_PATH = r"C:\Users\ashok\OneDrive\Desktop\4 - SEM SLAM\data"

df = pd.read_csv("dataset_with_transcripts.csv")

feature_dir = "../features"

os.makedirs(feature_dir, exist_ok=True)

features = []
labels = []

for idx, row in tqdm(df.iterrows(), total=len(df)):

    audio_path = os.path.join(BASE_DATA_PATH, row["audio_path"])

    try:
        audio, sr = librosa.load(audio_path, sr=16000)

        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=13
        )

        mfcc = mfcc.T

        feature_file = os.path.join(feature_dir, f"{idx}.npy")

        np.save(feature_file, mfcc)

        features.append(feature_file)
        labels.append(row["transcript"])

    except Exception as e:
        continue


output = pd.DataFrame({
    "feature_path": features,
    "transcript": labels
})

output.to_csv("training_dataset.csv", index=False)

print("Feature extraction complete:", len(output))