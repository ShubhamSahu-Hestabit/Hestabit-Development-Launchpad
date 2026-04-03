import os
import logging
import warnings
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_FILE = "logs/day2_orchestration.log"
_NOISY_LIBRARIES = ["httpx","httpcore","openai","openai._base_client","autogen_core","autogen_core.events","autogen_agentchat","sentence_transformers","sentence_transformers.SentenceTransformer","faiss","faiss.loader","transformers","torch","huggingface_hub","filelock","tqdm",]
def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("day2_orchestration")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    for lib in _NOISY_LIBRARIES:
        logging.getLogger(lib).setLevel(logging.CRITICAL + 1)
    return logger