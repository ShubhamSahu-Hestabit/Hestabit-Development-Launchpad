from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from config import model_client

research_agent = AssistantAgent(
    name="ResearchAgent",
    model_client=model_client,
    system_message="""
You are a Research Agent.

Your task is to gather factual information related to the user's query.

Rules:
- Provide research findings as bullet points
- Maximum 8 bullet points
- Each bullet must be under 20 words
- Focus only on factual information
- Do NOT summarize
- Do NOT provide conclusions
- Do NOT directly answer the question

Your output will be passed to the Summarizer Agent.
""",
    model_context=BufferedChatCompletionContext(buffer_size=10),
)