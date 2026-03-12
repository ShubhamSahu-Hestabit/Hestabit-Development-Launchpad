import os
import time
import json
import logging

from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel

from src.retriever.hybrid_retriever import HybridRetriever
from src.generator.llm_client import generate_answer
from src.memory.memory_store import MemoryStore
from src.evaluation.rag_eval import evaluate
from src.pipelines.sql_pipeline import run_sql_pipeline
from src.retriever.image_search import image_to_text_answer


# ==============================
# Logging Setup
# ==============================
os.makedirs("src/logs", exist_ok=True)

logging.basicConfig(
    filename="src/logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

FEEDBACK_FILE = "src/logs/FEEDBACK.json"

if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump([], f)


# ==============================
# Initialize App
# ==============================
app = FastAPI(title="Enterprise Knowledge Intelligence System")

retriever = HybridRetriever()
memory = MemoryStore()


# ==============================
# Request Schema
# ==============================
class Query(BaseModel):
    question: str


# ==============================
# TEXT RAG ENDPOINT (DAY-5 COMPLETE)
# ==============================
@app.post("/ask")
def ask(query: Query):
    start_time = time.time()

    memory.save("user", query.question)
    history = memory.get()

    results = retriever.search(query.question, top_k=5)
    contexts = [r["content"] for r in results]

    current_answer = generate_answer(query.question, contexts, history)

    max_attempts = 3
    threshold = 0.65

    best_answer = current_answer
    best_confidence = 0
    attempts_used = 1

    for attempt in range(max_attempts):

        confidence, hallucinated = evaluate(
            current_answer,
            contexts,
            query.question
        )

        if confidence > best_confidence:
            best_confidence = confidence
            best_answer = current_answer

        if confidence >= threshold:
            attempts_used = attempt + 1
            break

        current_answer = generate_answer(
            f"""
You are reviewing your previous answer.

Previous Answer:
{current_answer}

Instructions:
- Improve factual alignment with context.
- Remove unsupported claims.
- Be concise and precise.
""",
            contexts,
            history
        )

        attempts_used = attempt + 1

    memory.save("assistant", best_answer)

    latency = round(time.time() - start_time, 3)

    logger.info(f"Question: {query.question}")
    logger.info(f"Confidence: {best_confidence}")
    logger.info(f"Attempts Used: {attempts_used}")
    logger.info(f"Latency: {latency}")

    return {
        "answer": best_answer,
        "confidence": best_confidence,
        "hallucinated": best_confidence < threshold,
        "latency": latency,
        "attempts_used": attempts_used
    }


# ==============================
# SQL QA ENDPOINT
# ==============================
@app.post("/ask-sql")
def ask_sql(query: Query):
    answer = run_sql_pipeline(query.question)
    return {"answer": answer}


# ==============================
# IMAGE RAG ENDPOINT
# ==============================
@app.post("/ask-image")
async def ask_image(file: UploadFile):
    contents = await file.read()
    temp_path = "temp_uploaded_image.jpg"

    with open(temp_path, "wb") as f:
        f.write(contents)

    image_context = image_to_text_answer(temp_path)

    answer = generate_answer(
        "Explain this image in detail",
        [image_context],
        []
    )

    os.remove(temp_path)

    return {"answer": answer}


# ==============================
# HUMAN FEEDBACK ENDPOINT
# ==============================
@app.post("/feedback")
def feedback(
    question: str = Body(...),
    answer: str = Body(...),
    rating: int = Body(...),
    comment: str = Body(None)
):
    entry = {
        "timestamp": time.time(),
        "question": question,
        "answer": answer,
        "rating": rating,
        "comment": comment
    }

    with open(FEEDBACK_FILE, "r") as f:
        logs = json.load(f)

    logs.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    return {"message": "Feedback recorded successfully."}