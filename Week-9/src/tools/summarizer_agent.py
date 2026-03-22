from autogen_agentchat.agents import AssistantAgent
from config import model_client

summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    model_client=model_client,
    system_message=(
        "You are a summarization agent.\n"
        "Given raw output from multiple agents, produce a clean, concise summary.\n"
        "Highlight key findings, results, and any errors.\n"
        "Keep it under 10 lines. Use plain text, no markdown."
    )
)