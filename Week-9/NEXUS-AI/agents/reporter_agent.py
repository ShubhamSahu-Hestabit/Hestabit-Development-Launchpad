import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)

class ReporterAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Reporter",
            model_client=model_client,
            system_message=(
                "You are the Reporter agent.\n"
                "Compile comprehensive, production-ready documentation from all previous agent outputs.\n"
                "RULES:\n"
                "1. Include FULL DETAILS — do not summarize\n"
                "2. Preserve ALL code, diagrams, tables, and technical specifications\n"
                "3. Structure with clear markdown: ## Overview, ## Architecture, ## Implementation, ## Deployment, ## Recommendations\n"
                "4. Write as a standalone technical document — not as a summary of what agents did\n"
                "5. Your output is the FINAL DELIVERABLE — make it production-ready"
            ))

    async def run(self, content: str) -> str:
        logger.info("Reporter running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        return response.chat_message.content