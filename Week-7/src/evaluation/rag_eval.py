import os
import json
from datetime import datetime

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==============================
# Setup Logs
# ==============================
os.makedirs("src/logs", exist_ok=True)

MONITOR_FILE = "src/logs/EVAL-LOGS.json"

if not os.path.exists(MONITOR_FILE):
    with open(MONITOR_FILE, "w") as f:
        json.dump([], f)


# ==============================
# Load BGE Evaluation Model
# ==============================
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")


# ==============================
# Evaluation Function
# ==============================
def evaluate(answer, contexts, question):
    """
    Computes:
    - Context Match Score
    - Faithfulness Score
    - Hallucination Detection
    """

    context_text = " ".join(contexts)

    # Safety check
    if not context_text.strip():
        return 0.0, True

    # Encode (normalize for cosine stability)
    vec_answer = embedder.encode(
        answer,
        normalize_embeddings=True
    )

    vec_context = embedder.encode(
        context_text,
        normalize_embeddings=True
    )

    score = float(
        cosine_similarity(
            [vec_answer],
            [vec_context]
        )[0][0]
    )

    threshold = 0.65
    hallucinated = score < threshold
    confidence = round(score, 3)

    # Log evaluation
    entry = {
        "timestamp": str(datetime.utcnow()),
        "question": question,
        "confidence": confidence,
        "hallucinated": hallucinated
    }

    with open(MONITOR_FILE, "r") as f:
        logs = json.load(f)

    logs.append(entry)

    with open(MONITOR_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    return confidence, hallucinated