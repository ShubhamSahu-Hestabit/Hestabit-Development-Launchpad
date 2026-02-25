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
    import os
    client = Groq(api_key=os.environ.get(CONFIG["api_key_env"]))
else:
    raise ValueError("Unsupported provider")

# Function to generate answer
def generate_answer(question, contexts, history):
    context_text = "\n\n".join(contexts)

    prompt = f"""
You are an enterprise AI assistant.

Use ONLY the provided context.
If answer is not found in context, say: Not found in documents.

Context:
{context_text}

Conversation History:
{history}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=CONFIG["model_name"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content