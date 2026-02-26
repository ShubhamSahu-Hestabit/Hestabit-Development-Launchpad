import os
import json
import random
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer

# =====================================
# CONFIGURATION
# =====================================

DATASET_NAME = "Detsutut/MedInstruct"
MODEL_NAME = "gpt2"          # Safe public tokenizer
FINAL_SIZE = 1200
MAX_TOKEN_LENGTH = 512

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print(f"Loading dataset: {DATASET_NAME} ...")
dataset = load_dataset(DATASET_NAME, split="train")
print(f"Original dataset size: {len(dataset)}")

dataset = dataset.shuffle(seed=42)

# =====================================
# CLEANING + DEDUPLICATION
# =====================================

clean_data = []
seen = set()

def token_length(sample):
    text = (
        str(sample.get("instruction", "")) +
        str(sample.get("input", "")) +
        str(sample.get("output", ""))
    )
    return len(tokenizer.encode(text))

print("Cleaning dataset...")

for sample in dataset:
    instruction = str(sample.get("instruction", "")).strip()
    input_text = str(sample.get("input", "")).strip()
    output = str(sample.get("output", "")).strip()

    # Remove empty samples
    if not instruction or not output:
        continue

    item = {
        "instruction": instruction,
        "input": input_text,
        "output": output
    }

    key = json.dumps(item)

    # Remove duplicates
    if key not in seen:
        seen.add(key)
        clean_data.append(item)

print(f"After deduplication: {len(clean_data)}")

# =====================================
# TOKEN LENGTH ANALYSIS
# =====================================

print("Calculating token lengths...")
lengths = [token_length(x) for x in clean_data]

print("\nTOKEN STATS (Before Filtering)")
print("--------------------------------")
print(f"Mean: {np.mean(lengths):.2f}")
print(f"Median: {np.median(lengths)}")
print(f"Min: {np.min(lengths)}")
print(f"Max: {np.max(lengths)}")
print(f"95th Percentile: {np.percentile(lengths, 95)}")

# =====================================
# REMOVE LONG SAMPLES
# =====================================

filtered_data = [
    sample for sample, length in zip(clean_data, lengths)
    if length <= MAX_TOKEN_LENGTH
]

print(f"\nAfter removing > {MAX_TOKEN_LENGTH} tokens: {len(filtered_data)}")

if len(filtered_data) < FINAL_SIZE:
    raise ValueError(
        f"Not enough samples after filtering. Only {len(filtered_data)} remain."
    )

# =====================================
# SELECT FINAL 1200
# =====================================

final_data = random.sample(filtered_data, FINAL_SIZE)
print(f"Final dataset size selected: {len(final_data)}")

# =====================================
# SPLIT 70 / 15 / 15
# =====================================

train_end = int(0.70 * FINAL_SIZE)
val_end = int(0.85 * FINAL_SIZE)

train_data = final_data[:train_end]
val_data = final_data[train_end:val_end]
test_data = final_data[val_end:]

def save_jsonl(path, data):
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

save_jsonl(os.path.join(OUTPUT_DIR, "train.jsonl"), train_data)
save_jsonl(os.path.join(OUTPUT_DIR, "val.jsonl"), val_data)
save_jsonl(os.path.join(OUTPUT_DIR, "test.jsonl"), test_data)

print("\nFINAL SPLIT")
print("-----------")
print(f"Train: {len(train_data)}")
print(f"Validation: {len(val_data)}")
print(f"Test: {len(test_data)}")

print("\nDay-1 Completed Successfully (OOM Safe).")