# Week-8 Day-5 — Local LLM Capstone: Healthcare Assistant

A **production-ready local LLM deployment** using a quantized GGUF model, served via **FastAPI** with a **Streamlit UI** and optional **Docker** support.

---

## What's Built

| Component | File | Purpose |
|---|---|---|
| API Server | `deploy/app.py` | FastAPI with `/generate` + `/chat` |
| Model Loader | `deploy/model_loader.py` | Cached GGUF model loading |
| Config | `deploy/config.py` | Model path, params |
| UI | `streamlit_app.py` | Chat + Generate frontend |
| Container | `Dockerfile` | One-command deployment |

---

## Setup

```bash
cd ~/Hestabit-Development-Launchpad/Week-8/Day-5

# Optional: create venv
python3 -m venv venv && source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn llama-cpp-python pydantic streamlit requests
```

> **Model path:** Set in `deploy/config.py` → `models/model-q8_0.gguf`

---

## Run

### Backend API
```bash
uvicorn deploy.app:app --reload
```
Swagger docs → [http://localhost:8000/docs](http://localhost:8000/docs)

### Streamlit UI
```bash
streamlit run streamlit_app.py
```
- Toggle between **Chat** and **Generate** modes
- Tune `temperature`, `top-p`, `top-k` from sidebar
- **Clear chat** button resets session history

### Docker (one-command deploy)
```bash
docker build -t local-llm-api .
docker run -p 8000:8000 local-llm-api
```
Streamlit runs locally and connects to `localhost:8000`.

---

## API Endpoints

### `POST /generate`
Single-turn text generation.

```json
{
  "prompt": "Explain diabetes in simple terms.",
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "max_tokens": 256
}
```

### `POST /chat`
Multi-turn conversation with session memory.

```json
{
  "session_id": "user-001",
  "system": "You are a helpful healthcare assistant.",
  "message": "What are symptoms of hypertension?",
  "temperature": 0.7
}
```

Both endpoints support **streaming token output**.

---

## Screenshots

**FastAPI `/generate` endpoint**
![Generate Endpoint](images/fastapi_generate.png)

**FastAPI `/chat` endpoint**
![Chat Endpoint](images/fastapi_chat.png)

**Streamlit Chat UI**
![Chat UI](images/chat.png)

**Streamlit Generate UI**
![Generate UI](images/generate.png)

---

## Notes

- Chat history is maintained **per session_id**
- Model is loaded once and cached — no cold-start per request
- System + user prompts handled separately for clean templating
- Streaming works for both endpoints

