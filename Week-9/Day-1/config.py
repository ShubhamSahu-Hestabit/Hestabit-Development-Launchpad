from autogen_ext.models.ollama import OllamaChatCompletionClient
from logger_config import setup_logger

logger = setup_logger()
try:
    model_client = OllamaChatCompletionClient(
        model="qwen2.5:7b-instruct-q4_0",
        options={"temperature": 0.2},
    )
    ACTIVE_MODEL = "OLLAMA (qwen2.5:7b-instruct-q4_0)"
    logger.info(f"ACTIVE MODEL -> {ACTIVE_MODEL}")
except Exception as e:
    logger.exception("Failed to initialize Ollama model client")
    raise RuntimeError(
        "Could not initialize local Ollama model. "
        "Make sure Ollama is running and the model is available."
    ) from e