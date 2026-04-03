import os
from dotenv import load_dotenv
from logger_config import setup_logger
load_dotenv()
logger = setup_logger()
try:
    from autogen_ext.models.openai import OpenAIChatCompletionClient
except Exception:
    OpenAIChatCompletionClient = None
try:
    from autogen_ext.models.ollama import OllamaChatCompletionClient
except Exception:
    OllamaChatCompletionClient = None
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY and OpenAIChatCompletionClient:
    model_client = OpenAIChatCompletionClient(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model_info={
            "family": "openai",
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
        },
    )
    ACTIVE_MODEL = "GROQ (llama-3.3-70b-versatile)"
elif OllamaChatCompletionClient:
    model_client = OllamaChatCompletionClient(
        model="qwen2.5:7b-instruct-q4_0",
        options={"temperature": 0.2},
    )
    ACTIVE_MODEL = "OLLAMA (qwen2.5:7b-instruct-q4_0)"
else:
    raise RuntimeError("No model client available. Set GROQ_API_KEY or install Ollama.")
logger.info(f"ACTIVE MODEL -> {ACTIVE_MODEL}")