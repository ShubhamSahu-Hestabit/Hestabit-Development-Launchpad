from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.models import SystemMessage, UserMessage
from config import model_client
from logger_config import setup_logger
from orchestrator.messages import ValidationResult, ValidationTask

logger = setup_logger()
class ValidatorAgent(RoutedAgent):
    def __init__(self):
        super().__init__(description="Validator Agent")
        self._model_client = model_client
    @message_handler
    async def handle_task(self, message: ValidationTask, ctx: MessageContext) -> ValidationResult:
        logger.info("Validation started")
        system_prompt = (
            "You are a Validator Agent.\n"
            "Check whether the answer actually solves the user's request.\n"
            "Validate accuracy, completeness, consistency, relevance, and clarity.\n"
            "Strictly check whether hard constraints in the user's request are satisfied.\n"
            "If the answer is too generic or violates the user's constraints, mark FAIL.\n"
            "Respond exactly in this format:\n"
            "VALIDATION: PASS or FAIL\n"
            "FINAL_RESULT:\n"
            "<approved or corrected answer>\n"
        )
        user_prompt = f"Task:\n{message.original_task}\n\nAnswer:\n{message.reflected_result}"
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt, source="user"),
        ]
        result = await self._model_client.create(messages)
        text = str(result.content)
        is_valid = True
        final_result = message.reflected_result
        lines = text.splitlines()
        capture_final = False
        final_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.upper().startswith("VALIDATION:"):
                is_valid = "PASS" in stripped.upper()
            elif stripped.upper().startswith("FINAL_RESULT:"):
                capture_final = True
                after_colon = stripped.split(":", 1)[1].strip()
                if after_colon:
                    final_lines.append(after_colon)
            elif capture_final:
                final_lines.append(line)
        if final_lines:
            final_result = "\n".join(final_lines).strip()
        print("\nValidation:", "PASS" if is_valid else "FAIL")
        logger.info(f"Validation completed | status={'PASS' if is_valid else 'FAIL'}")
        return ValidationResult(
            is_valid=is_valid,
            final_result=final_result,
        )