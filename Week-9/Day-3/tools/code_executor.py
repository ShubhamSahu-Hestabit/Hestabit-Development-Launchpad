import logging
import re
from typing import Any
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from config import model_client

logger = logging.getLogger(__name__)
executor = LocalCommandLineCodeExecutor()
code_agent = AssistantAgent(
    name="CodeExecutorAgent",
    model_client=model_client,
    system_message=(
        "You are a Python code generator.\n\n"
        "Return ONLY executable Python code.\n"
        "Do not return JSON.\n"
        "Do not explain anything.\n"
        "Do not add markdown fences.\n"
        "Do not add expected output.\n"
        "Always use proper indentation.\n"
        "Always print final results using print().\n"
        "Never compress logic into one line.\n"
        "Write safe, error-free Python.\n\n"

        "When working with CSV data:\n"
        "- If csv_data is provided, use it directly.\n"
        "- Parse it with io.StringIO and pandas.\n"
        "- Do not recreate the dataset manually.\n"
        "- Use safe pandas indexing.\n"
        "- Never use df.loc[-1]; use df.iloc[-1] for the last row.\n\n"

        "Style example:\n"
        "def is_palindrome(n):\n"
        "    if str(n) == str(n)[::-1]:\n"
        "        return True\n"
        "    else:\n"
        "        return False\n"
    ),
)
def _clean_code(text: str) -> str:
    """
    Extract only executable Python code.
    Removes markdown fences, markdown/output sections, and stray printed-output lines.
    """
    text = str(text)
    text = re.sub(r"```markdown.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"```python", "", text)
    text = re.sub(r"```", "", text)
    text = re.sub(r"\nmarkdown\b.*", "", text, flags=re.DOTALL)
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# Output"):
            continue
        if stripped.startswith("Output:"):
            continue
        if stripped.startswith("Here is"):
            continue
        if stripped.startswith("When you run"):
            continue
        if stripped.startswith("Number:"):
            continue
        if " is a palindrome" in stripped and not stripped.startswith("print"):
            continue
        if "Palindrome:" in stripped and not stripped.startswith("print"):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()
async def run_code_task(task: str) -> str:
    try:
        result = await code_agent.run(task=task)
        raw_output: Any = result.messages[-1].content
        code = _clean_code(str(raw_output))
        logger.info(f"Generated code:\n{code}")
        if not code.strip():
            return "ERROR: No executable Python code was generated."
        exec_result = await executor.execute_code_blocks(
            [CodeBlock(code=code, language="python")],
            CancellationToken(),
        )
        output = getattr(exec_result, "output", "")
        return str(output).strip() if output is not None else ""
    except Exception as e:
        logger.exception("Code execution failed")
        return f"ERROR: {str(e)}"