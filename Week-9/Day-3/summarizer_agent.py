from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from config import model_client

summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    model_client=model_client,
    system_message="""
You are a Summarizer Agent.
Your job is to summarize research findings.
Rules:
- Convert the bullet points into ONE concise paragraph
- Maximum 80 words
- Focus only on key insights
- Do NOT repeat bullet formatting
- Do NOT add new information
- Do NOT answer the question
The summary will be passed to the Answer Agent.
""",
    model_context=BufferedChatCompletionContext(buffer_size=10),
)