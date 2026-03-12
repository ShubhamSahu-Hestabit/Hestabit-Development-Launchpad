from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uuid
import logging

from deploy.model_loader import load_model

app = FastAPI(
    title="Local LLM API",
    description="Quantized GGUF model inference server"
)

logging.basicConfig(level=logging.INFO)

llm = load_model()
chat_sessions = {}

# ------------------------
# Request Schemas
# ------------------------
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 200
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40

class ChatRequest(BaseModel):
    session_id: str
    system_prompt: str
    message: str
    max_tokens: int = 200
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40

# ------------------------
# Generate Endpoint
# ------------------------
@app.post("/generate")
def generate(req: GenerateRequest):

    request_id = str(uuid.uuid4())
    logging.info(f"[{request_id}] Generate request received")

    def stream():
        for token in llm(
            req.prompt,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            top_k=req.top_k,
            stream=True
        ):
            text = token["choices"][0].get("text", "")
            yield text

    return StreamingResponse(stream(), media_type="text/plain")


# ------------------------
# Chat Endpoint
# ------------------------
@app.post("/chat")
def chat(req: ChatRequest):

    request_id = str(uuid.uuid4())
    logging.info(f"[{request_id}] Chat request | session={req.session_id}")

    if req.session_id not in chat_sessions:
        chat_sessions[req.session_id] = []

    history = chat_sessions[req.session_id]

    prompt = f"""
System: {req.system_prompt}

Conversation History:
{history}

User: {req.message}

Assistant:
"""

    def stream():
        response_text = ""
        for token in llm(
            prompt,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            top_k=req.top_k,
            stream=True
        ):
            text = token["choices"][0].get("text", "")
            response_text += text
            yield text

        # Append to history
        history.append({
            "user": req.message,
            "assistant": response_text
        })

    return StreamingResponse(stream(), media_type="text/plain")