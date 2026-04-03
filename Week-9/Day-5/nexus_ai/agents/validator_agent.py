import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)
class ValidatorAgent:
    """
    Verifies outputs meet requirements.
    Returns readable text verdict — not JSON — so Reporter can use it as context.
    """
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Validator",
            model_client=model_client,
            system_message=(
                "You are the Validator agent.\n"
                "Verify outputs meet all requirements and acceptance criteria.\n"
                "Check: correctness, completeness, edge cases, consistency.\n"
                "\n"
                "Return a clear verdict:\n"
                "- PASS: output is correct and complete\n"
                "- IMPROVE: output has minor issues (list them)\n"
                "- FAIL: output has major issues (list them)\n"
                "\n"
                "Be specific about what passes and what needs improvement.\n"
                "Do NOT generate new content beyond validation feedback."
            ))
    async def run(self, content: str) -> str:
        logger.info("Validator running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content