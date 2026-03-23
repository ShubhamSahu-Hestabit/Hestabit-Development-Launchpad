import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)


class PlannerAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Planner",
            model_client=model_client,
            system_message=("""You are the Planner agent.
Your task is to decompose user goals into detailed, ordered execution steps.

Rules:
1. Create 8-12 steps for complex tasks
2. Assign each step to ONE agent: Researcher, Analyst, Coder, Critic, Optimizer, Validator, Reporter
3. Make tasks SPECIFIC and DETAILED
4. Reporter must always be the LAST step

Output ONLY valid JSON in this format:
{
  "steps": [
    {"agent": "Researcher", "task": "detailed task description"},
    {"agent": "Reporter", "task": "compile all outputs into final document"}
  ]
}

No other text. Only JSON."""
            ))

    async def run(self, content: str) -> str:
        logger.info(f"Planner running for: {content[:80]}")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")],
            cancellation)
        return response.chat_message.content