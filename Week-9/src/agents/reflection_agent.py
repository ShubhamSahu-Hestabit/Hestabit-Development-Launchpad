from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage
from orchestrator.messages import ReflectionTask, ReflectionResult
from config import model_client

class ReflectionAgent(RoutedAgent):
    def __init__(self):
        super().__init__(description="Reflection Agent - Quality Improvement")
        self._model_client = model_client
    @message_handler
    async def handle_task(self, message: ReflectionTask, ctx: MessageContext) -> ReflectionResult:
        combined = "\n\n".join([
            f"Worker {i+1} (Agent: {wr.agent_id}, Subtask: {wr.subtask_id}):\n{wr.result}"
            for i, wr in enumerate(message.worker_results)
        ])
        prompt = (
            "You are a Reflection Agent.\n\n"
            "Analyze the outputs from multiple workers.\n"
            "Identify contradictions, missing information, and best insights.\n"
            "Then synthesize a single superior answer that is logically consistent and complete.\n\n"
            "Worker outputs:\n" + combined
        )
        messages = [
            SystemMessage(content=prompt),
            UserMessage(
                content=f"Original task: {message.original_task}\n\nSynthesize the outputs.",
                source="user",
            ),
        ]
        model_result = await self._model_client.create(messages)
        result_text = str(model_result.content)
        print(f"\n{'='*80}")
        print(f"Reflection-{self.id.key}")
        print(f"{'-'*80}")
        print(result_text[:300] + "...")
        print(f"{'='*80}\n")
        return ReflectionResult(refined_result=result_text)