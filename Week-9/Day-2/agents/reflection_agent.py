from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.models import SystemMessage, UserMessage
from config import model_client
from logger_config import setup_logger
from orchestrator.messages import ReflectionResult, ReflectionTask

logger = setup_logger()
class ReflectionAgent(RoutedAgent):
    def __init__(self):
        super().__init__(description="Reflection Agent")
        self._model_client = model_client
    @message_handler
    async def handle_task(self, message: ReflectionTask, ctx: MessageContext) -> ReflectionResult:
        logger.info("Reflection started")
        combined = "\n\n".join(
            f"Worker {i+1} (Agent: {wr.agent_id}, Subtask: {wr.subtask_id}):\n{wr.result}"
            for i, wr in enumerate(message.worker_results)
        )
        system_prompt = (
            "You are a Reflection Agent.\n"
            "Combine worker outputs into one final user-facing answer.\n"
            "Ensure completeness, consistency, and clarity.\n"
            "Preserve all original user constraints.\n"
            "Reconcile partial results into one coherent solution.\n"
            "If worker outputs conflict with a hard constraint, revise the answer to stay within that constraint.\n"
            "Do NOT invent unsupported facts.\n"
            "Produce the actual final answer, not a meta-summary.\n"
        )
        user_prompt = f"Original Task:\n{message.original_task}\n\nWorker Outputs:\n{combined}"
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt, source="user"),
        ]
        result = await self._model_client.create(messages)
        output = str(result.content)
        print("\nReflection")
        print("-" * 40)
        print(output[:300] + ("..." if len(output) > 300 else ""))
        logger.info("Reflection completed")
        return ReflectionResult(refined_result=output)