import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from tools.web_search import get_compound_client

logger = logging.getLogger(__name__)
class ResearcherAgent:
    """Uses compound-beta — built-in web search, no external tools needed."""
    def __init__(self, model_client):
        try:
            client = get_compound_client()
            logger.info("Researcher using compound-beta (web search)")
        except Exception as e:
            logger.warning(f"compound-beta unavailable, falling back: {e}")
            client = model_client

        self.agent = AssistantAgent(
            name="Researcher",
            model_client=client,
            system_message=(
                "You are the Researcher agent.\n"
                "Use web search to find accurate, current information.\n"
                "Focus on best practices, latest tools, benchmarks.\n"
                "Always search before answering.\n"
                "Do not write code or make final decisions.\n"
                "Present findings clearly with sources noted."
            ))
    async def run(self, content: str) -> str:
        logger.info("Researcher running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content