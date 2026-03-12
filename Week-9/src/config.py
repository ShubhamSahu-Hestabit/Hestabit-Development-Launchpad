from autogen_ext.models.ollama import OllamaChatCompletionClient

# Shared Ollama model client
model_client = OllamaChatCompletionClient(
    model="qwen2.5:7b-instruct-q4_0",
    options={
        "temperature": 0.3,
        "num_predict": 200
    }
)