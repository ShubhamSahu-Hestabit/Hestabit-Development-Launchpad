import os
import sys
import logging
import warnings
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
os.makedirs("logs", exist_ok=True)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL + 1)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
file_handler = logging.FileHandler("logs/nexus.log", mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
for lib in [
    "httpx", "httpcore", "openai", "openai._base_client",
    "autogen_core", "autogen_core.events", "autogen_agentchat",
    "sentence_transformers", "sentence_transformers.SentenceTransformer",
    "faiss", "faiss.loader",
    "transformers", "torch",
    "huggingface_hub", "filelock", "tqdm",
]:
    logging.getLogger(lib).setLevel(logging.CRITICAL + 1)
logger = logging.getLogger(__name__)
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
            "context_length": 131072,
        }
    )
    ACTIVE_MODEL = "GROQ (llama-3.3-70b-versatile)"
elif OllamaChatCompletionClient:
    model_client = OllamaChatCompletionClient(
        model="qwen2.5:7b-instruct-q4_0",
        options={"temperature": 0.2}
    )
    ACTIVE_MODEL = "OLLAMA (qwen2.5:7b-instruct-q4_0)"
else:
    raise RuntimeError("No model client available. Set GROQ_API_KEY or install Ollama.")
logger.info(f"ACTIVE MODEL → {ACTIVE_MODEL}")