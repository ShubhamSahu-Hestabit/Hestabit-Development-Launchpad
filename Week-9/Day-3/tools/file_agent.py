import os
import logging
from typing_extensions import Annotated
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from config import model_client

logger = logging.getLogger(__name__)
BASE_DIR = os.path.abspath(".")
def resolve_path(file_name: str) -> str:
    return os.path.join(BASE_DIR, file_name)
async def read_file(file_path: Annotated[str, "File name only, e.g. sales.csv"]) -> str:
    if "." not in file_path:
        return "ERROR: Provide valid file name like sales.csv"
    safe_path = resolve_path(file_path)
    if not os.path.exists(safe_path):
        logger.error(f"File not found: {safe_path}")
        return f"ERROR: File not found → {file_path}"
    if file_path.endswith(".csv") or file_path.endswith(".txt"):
        logger.info(f"Reading file: {safe_path}")
        with open(safe_path, "r", encoding="utf-8") as f:
            return f.read()
    logger.warning(f"Unsupported file: {file_path}")
    return "ERROR: Only .csv and .txt supported"
async def write_file(
    file_path: Annotated[str, "File name, e.g. output.txt"],
    content: Annotated[str, "Plain text content to write into the file"]
) -> str:
    if "." not in file_path:
        return "ERROR: Invalid file name"
    safe_path = resolve_path(file_path)
    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(str(content))
        logger.info(f"Wrote file: {safe_path}")
        return f"SUCCESS: Written to {file_path}"
    except Exception as e:
        logger.error(str(e))
        return f"ERROR: {str(e)}"
read_tool = FunctionTool(
    read_file,
    description="Read a CSV or TXT file. Pass only the filename, e.g. sales.csv"
)
write_tool = FunctionTool(
    write_file,
    description="Write plain text content to a file. Pass filename and content as plain string."
)
file_agent = AssistantAgent(
    name="FileAgent",
    tools=[read_tool, write_tool],
    model_client=model_client,
    system_message=(
        "You are a file processing agent.\n"
        "Use read_file to read files. Use write_file to write files.\n"
        "Pass content as a plain string — no special formatting or escaping.\n"
        "Read only .csv and .txt files.\n"
        "Write only .txt or .csv files.\n"
    )
)