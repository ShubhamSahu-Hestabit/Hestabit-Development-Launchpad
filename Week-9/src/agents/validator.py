from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage
from orchestrator.messages import ValidationTask, ValidationResult
from config import model_client


class ValidatorAgent(RoutedAgent):

    def __init__(self):
        super().__init__(description="Validator Agent - Quality Assurance")
        self._model_client = model_client

    @message_handler
    async def handle_task(self, message: ValidationTask, ctx: MessageContext) -> ValidationResult:

        system_prompt = (
            "You are a Validator Agent responsible for quality assurance.\n\n"
            "Check for:\n"
            "1. Accuracy\n"
            "2. Completeness\n"
            "3. Logical consistency\n"
            "4. Relevance\n"
            "5. Clarity\n\n"
            "Respond in format:\n"
            "VALIDATION: PASS or FAIL\n"
            "FINAL_RESULT: corrected or approved answer\n"
        )

        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(
                content=f"Original Task:\n{message.original_task}\n\n"
                f"Result to Validate:\n{message.reflected_result}",
                source="user",
            ),
        ]

        model_result = await self._model_client.create(messages)

        validation_text = str(model_result.content)

        is_valid = "fail" not in validation_text.lower()

        final_result = message.reflected_result

        for line in validation_text.split("\n"):
            if line.startswith("FINAL_RESULT"):
                final_result = line.split(":", 1)[1].strip()

        print(f"\n{'='*80}")
        print(f"Validator-{self.id.key}")
        print(f"{'-'*80}")
        print(f"Validation Status: {'PASS' if is_valid else 'FAIL'}")
        print(f"{'='*80}\n")

        return ValidationResult(
            is_valid=is_valid,
            final_result=final_result,
        )