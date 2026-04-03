import os
import logging
logger = logging.getLogger(__name__)

def get_compound_client():
    """
    Groq compound-beta — built-in web search via Tavily.
    No extra packages. Uses existing GROQ_API_KEY.
    Only for Researcher — does NOT support external tool calling.
    """
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        client = OpenAIChatCompletionClient(
            model="compound-beta",
            api_key=os.getenv("GROQ_API_KEY"),
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
        logger.info("compound-beta client created (web search enabled)")
        return client
    except Exception as e:
        logger.error(f"compound-beta failed: {e}")
        raise