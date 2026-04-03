from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.models import SystemMessage, UserMessage
from config import model_client
from logger_config import setup_logger
from orchestrator.messages import WorkerResult, WorkerTask

logger = setup_logger()
class WorkerAgent(RoutedAgent):
    def __init__(self):
        super().__init__(description="Worker Agent")
        self._model_client = model_client
    @message_handler
    async def handle_task(self, message: WorkerTask, ctx: MessageContext) -> WorkerResult:
        logger.info(f"Worker started | subtask={message.subtask_id}")
        print(f"\nWorker: {message.subtask_id}")
        print("-" * 40)
        print(message.task)
        dependency_context = ""
        if message.previous_results:
            dependency_context = "\nDEPENDENCY RESULTS:\n" + "\n\n".join(message.previous_results)
        system_prompt = (
            "You are an expert task execution agent.\n"
            "You receive a MAIN TASK, a SUBTASK, and optional dependency results.\n"
            "Solve only the assigned SUBTASK while keeping the MAIN TASK objective in mind.\n"
            "Preserve all original user requirements and hard constraints.\n"
            "Do NOT assume that global constraints belong entirely to your subtask.\n"
            "Treat limits such as budget, duration, quantity, and scope as shared across the full solution.\n"
            "Use dependency results only when relevant.\n"
            "Do NOT ask the user for more information.\n"
            "Return a practical and specific partial result for your subtask.\n"
        )
        user_prompt = f"{message.task}\n{dependency_context}\n\nProvide a concise solution."
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt, source="worker"),
        ]
        result = await self._model_client.create(messages)
        output = str(result.content)
        print(output[:500] + ("..." if len(output) > 500 else ""))
        logger.info(f"Worker completed | subtask={message.subtask_id}")
        return WorkerResult(
            subtask_id=message.subtask_id,
            agent_id=self.id.key,
            result=output,
        )