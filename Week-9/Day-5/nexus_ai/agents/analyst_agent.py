import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)
class AnalystAgent:
    """
    Receives computed data from Coder via context.
    Interprets actual numbers into real business insights.
    Never gives generic or theoretical insights.
    """
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Analyst",
            model_client=model_client,
            system_message=(
                "You are the Analyst agent.\n"
                "You receive COMPUTED data and statistics from Coder.\n"
                "Your job is to interpret those REAL NUMBERS into insights.\n"
                "\n"
                "RULES:\n"
                "1. Use ONLY the actual numbers from PREVIOUS STEP\n"
                "2. Every insight must reference a specific number or value\n"
                "3. NEVER give generic insights like 'data shows trends'\n"
                "4. NEVER say 'further analysis needed'\n"
                "5. Be specific: 'Product J has highest sales of 1000'\n"
                "   not 'some products perform better than others'\n"
                "6. Do NOT write code\n"
                "7. Do NOT save files\n"
                "\n"
                "GOOD insight example:\n"
                "   'Product J leads with SalesAmount of 1000, which is 10x\n"
                "    higher than Product A at 100'\n"
                "\n"
                "BAD insight example:\n"
                "   'The data shows potential for further analysis'"
            ))

    async def run(self, content: str) -> str:
        logger.info("Analyst running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content