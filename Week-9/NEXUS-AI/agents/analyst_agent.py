import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)

class AnalystAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Analyst",
            model_client=model_client,
            system_message=(
                "You are the Analyst agent.\n"
                "Analyze problems, evaluate trade-offs, performance, scalability, and risks.\n"
                "Verify logic, assumptions, and expected behavior.\n"
                "Do NOT write production code.\n"
                "Focus on correctness, feasibility, and implications."
            ))

    async def run(self, content: str) -> str:
        logger.info("Analyst running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content