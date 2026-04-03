import logging
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)
OUTPUT_DIR = os.path.abspath("outputs")
class ReporterAgent:
    """
    No tools — avoids Groq tool calling bugs.
    Detects SAVE_FILE: instruction in response and handles writing directly in Python.
    """
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Reporter",
            model_client=model_client,
            system_message=(
                "You are the Reporter agent.\n"
                "Compile all previous agent outputs into a clear final answer.\n"
                "\n"
                "DEFAULT — return the complete answer as text in your response.\n"
                "\n"
                "ONLY when task EXPLICITLY says save/create a file:\n"
                "Write the full file content first, then on the LAST LINE write:\n"
                "SAVE_FILE: filename.csv\n"
                "or SAVE_FILE: filename.txt\n"
                "\n"
                "NEVER add SAVE_FILE unless task explicitly says save/create a file.\n"
                "NEVER save .md files.\n"
                "Your response text IS the final output shown to the user."
            ))
    async def run(self, content: str) -> str:
        logger.info("Reporter running")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)
        result = response.chat_message.content
        return self._handle_file_save(result)
    def _handle_file_save(self, content: str) -> str:
        """Detect SAVE_FILE instruction, save the file, clean response."""
        lines = content.strip().split('\n')
        save_line = None
        save_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("SAVE_FILE:"):
                save_line = line.strip()
                save_index = i
                break
        if not save_line:
            return content
        filename = save_line.replace("SAVE_FILE:", "").strip()
        file_content = '\n'.join(lines[:save_index]).strip()
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            filepath = os.path.join(OUTPUT_DIR, os.path.basename(filename))
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content)
            logger.info(f"File saved: {filepath}")
            return f"{file_content}\n\nFile saved → outputs/{os.path.basename(filename)}"
        except Exception as e:
            logger.error(f"File save failed: {e}")
            return content