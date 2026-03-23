import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)

class CoderAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Coder",
            model_client=model_client,
            system_message=(
                "You are the Coder agent.\n"
                "Write clean, correct, efficient code based on specifications.\n"
                "Do NOT change requirements or invent features.\n"
                "Include comments for clarity.\n"
                "Follow best practices for readability and maintainability."
            ))

    async def run(self, content: str) -> str:
        logger.info("Coder running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content