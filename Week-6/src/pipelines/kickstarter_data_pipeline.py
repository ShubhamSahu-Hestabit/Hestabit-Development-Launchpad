import pandas as pd
from sklearn.model_selection import train_test_split

# ----------------------------
# 1. Load original dataset
# ----------------------------
DATA_PATH = "/home/shubhamsahu/Hestabit-Development Launchpad/Week-6/src/data/raw/kickstarter.csv"

df = pd.read_csv(DATA_PATH)

print("Total rows in original dataset:", len(df))
print("\nState distribution:")
print(df["state"].value_counts())

# ----------------------------
# 2. Filter successful & failed
# ----------------------------
df_binary = df[df["state"].isin(["successful", "failed"])].copy()

print("\nRows after filtering successful & failed:", len(df_binary))
print("\nBinary distribution:")
print(df_binary["state"].value_counts())

# ----------------------------
# 3. Create binary target
# ----------------------------
df_binary["target"] = df_binary["state"].apply(
    lambda x: 1 if x == "successful" else 0
)

print("\nTarget distribution:")
print(df_binary["target"].value_counts())

# ----------------------------
# 4. Stratified Sampling (30K)
# ----------------------------
sample_size = 30000

df_sampled, _ = train_test_split(
    df_binary,
    train_size=sample_size,
    stratify=df_binary["target"],
    random_state=42
)

print("\nSampled dataset size:", len(df_sampled))
print("\nSampled target distribution:")
print(df_sampled["target"].value_counts(normalize=True))

# ----------------------------
# 5. Save as official raw dataset
# ----------------------------
OUTPUT_PATH = "/home/shubhamsahu/Hestabit-Development Launchpad/Week-6/src/data/raw/kickstarter_30k.csv"

df_sampled.to_csv(OUTPUT_PATH, index=False)

print("\n✅ Saved kickstarter_30k.csv")
