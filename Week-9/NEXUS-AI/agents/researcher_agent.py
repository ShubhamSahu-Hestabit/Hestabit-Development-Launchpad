import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)

class ResearcherAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Researcher",
            model_client=model_client,
            system_message=(
                "You are the Researcher agent.\n"
                "Gather accurate, relevant information needed to complete assigned tasks.\n"
                "Focus on best practices, algorithms, libraries, APIs, and prior art.\n"
                "Do not write code or make final decisions.\n"
                "Present findings clearly with assumptions and limitations noted."
            ))

    async def run(self, content: str) -> str:
        logger.info("Researcher running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content