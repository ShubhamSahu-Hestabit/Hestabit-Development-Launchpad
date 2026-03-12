from llama_cpp import Llama
from functools import lru_cache
from deploy.config import GGUF_MODEL_PATH, MAX_CONTEXT

@lru_cache()
def load_model():
    model = Llama(
        model_path=GGUF_MODEL_PATH,
        n_ctx=MAX_CONTEXT
    )
    return model