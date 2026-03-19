from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage

from orchestrator.messages import WorkerTask, WorkerResult
from config import model_client

class WorkerAgent(RoutedAgent):

    def __init__(self):
        super().__init__(description="Worker Agent")
        self._model_client = model_client

    @message_handler
    async def handle_task(self, message: WorkerTask, ctx: MessageContext) -> WorkerResult:

        print("\n" + "=" * 80)
        print(f"{self.id.type}-{self.id.key} (Subtask: {message.subtask_id})")
        print("-" * 80)

        system_prompt = (
            "You are an expert task execution agent.\n"
            "You will receive a MAIN TASK and a SUBTASK.\n"
            "Solve the SUBTASK while keeping the MAIN TASK objective in mind.\n"
            "Do NOT ask the user for additional information.\n"
            "Make reasonable assumptions if details are missing.\n"
            "Return a clear, structured, and practical answer.\n"
        )

        user_prompt = f"""
Solve the following task.

{message.task}

Provide a concise and useful solution.
"""

        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt, source="worker"),
        ]

        result = await self._model_client.create(messages)

        output = str(result.content)

        preview = output[:500]
        print(preview)

        if len(output) > 500:
            print("...")

        print("=" * 80)

        return WorkerResult(
            subtask_id=message.subtask_id,
            agent_id=self.id.key,
            result=output,
        )