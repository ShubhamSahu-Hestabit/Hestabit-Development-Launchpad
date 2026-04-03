import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Absolute path to model.yaml
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "model.yaml")

# Read YAML
with open(CONFIG_FILE, "r") as f:
    CONFIG = yaml.safe_load(f)

# Load GROQ client if provider is groq
if CONFIG["provider"] == "groq":
    from groq import Groq

    api_key = os.environ.get(CONFIG["api_key_env"])
    if not api_key:
        raise ValueError(f"Missing API key in environment variable: {CONFIG['api_key_env']}")

    client = Groq(api_key=api_key)
else:
    raise ValueError("Unsupported provider")


# Function to generate answer
def generate_answer(question, contexts, history):
    context_text = "\n\n".join(contexts)

    prompt = f"""
You are an enterprise AI assistant.

- Use the provided context as the primary source.
- If the context contains relevant information, answer clearly and naturally.
- If the context is not sufficient, say:
  "This question is outside the scope of the provided documents."

Do NOT list unrelated items.
Context:
{context_text}

Conversation History:
{history}

Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model=CONFIG["model_name"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        # Safe response extraction
        if response and hasattr(response, "choices") and len(response.choices) > 0:
            message = response.choices[0].message
            if message and message.content:
                return message.content
            else:
                return "Error: Empty message content from LLM."
        else:
            return "Error: Empty response from LLM."

    except Exception as e:
        # Minimal logging (helps debugging)
        print(f"[ERROR] LLM call failed: {str(e)}")

        error_message = str(e).lower()

        if "api_key" in error_message or "authentication" in error_message:
            return "Error: Invalid or expired API key."

        elif "rate limit" in error_message:
            return "Error: Rate limit exceeded. Please try again later."

        elif "timeout" in error_message:
            return "Error: Request timed out. Please retry."

        else:
            return f"Error: LLM service failed -> {str(e)}"