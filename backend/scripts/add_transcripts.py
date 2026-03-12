import pandas as pd

# Load dataset index
df = pd.read_csv("dataset_index.csv")

# Word mapping (temporary small vocabulary)
label_map = {
    "C1": "yes",
    "C2": "no",
    "C3": "hello",
    "C4": "thank",
    "C5": "you",
    "C6": "please",
    "C7": "good",
    "C8": "morning"
}

# Convert labels to words
df["transcript"] = df["label"].map(label_map)

# Remove rows where transcript not available
df = df.dropna()

# Save new dataset
df.to_csv("dataset_with_transcripts.csv", index=False)

print("New dataset created:", len(df))