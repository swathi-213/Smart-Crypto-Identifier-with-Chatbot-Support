import pandas as pd
from pathlib import Path
from modules.module1_features import extract_features

DATASET_DIR = Path("data/raw")
rows = []

for algo_dir in DATASET_DIR.iterdir():
    if not algo_dir.is_dir():
        continue

    algorithm = algo_dir.name
    print(f"Processing {algorithm}")

    for file in algo_dir.iterdir():
        if file.is_file():
            byte_data = file.read_bytes()
            feats = extract_features(byte_data)
            feats["algorithm"] = algorithm
            rows.append(feats)

df = pd.DataFrame(rows)
df.to_csv("features_enhanced.csv", index=False)

print("✅ features_enhanced.csv created")
print("Total samples:", len(df))