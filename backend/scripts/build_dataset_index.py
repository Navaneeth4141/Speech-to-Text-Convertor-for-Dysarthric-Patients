import os
import pandas as pd

BASE_PATH = r"C:\Users\ashok\OneDrive\Desktop\4 - SEM SLAM\data"

rows = []

datasets = [
    "noisereduced-uaspeech",
    "noisereduced-uaspeech-control"
]

for dataset in datasets:

    dataset_path = os.path.join(BASE_PATH, dataset)

    for speaker in os.listdir(dataset_path):

        speaker_path = os.path.join(dataset_path, speaker)

        if not os.path.isdir(speaker_path):
            continue

        for file in os.listdir(speaker_path):

            if file.endswith(".wav"):

                parts = file.split("_")

                label = parts[2]

                rows.append({
                    "audio_path": os.path.join(dataset, speaker, file),
                    "label": label
                })


df = pd.DataFrame(rows)

df.to_csv("dataset_index.csv", index=False)

print("Dataset index created:", len(df))