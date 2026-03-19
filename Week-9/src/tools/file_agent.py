import os
import logging
import pandas as pd
import io
from typing_extensions import Annotated
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from config import model_client

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath("src")

def resolve_path(file_name: str) -> str:
    return os.path.join(BASE_DIR, file_name)


async def read_file(file_path: Annotated[str, "File name only"]) -> str:
    if "." not in file_path:
        return "ERROR: Provide valid file name like sales.csv"

    safe_path = resolve_path(file_path)

    if not os.path.exists(safe_path):
        logger.error(f"File not found: {safe_path}")
        return f"ERROR: File not found → {file_path}"

    if file_path.endswith(".csv") or file_path.endswith(".txt"):
        logger.info(f"Reading file: {safe_path}")
        with open(safe_path, "r") as f:
            return f.read()

    logger.warning(f"Unsupported file: {file_path}")
    return "ERROR: Only .csv and .txt supported"


async def write_file(file_path: Annotated[str, "File name"], content: Annotated[str, "Content"]) -> str:
    if "." not in file_path:
        return "ERROR: Invalid file name"

    safe_path = resolve_path(file_path)

    try:
        if file_path.endswith(".txt"):
            with open(safe_path, "w") as f:
                f.write(content)

        elif file_path.endswith(".csv"):
            df = pd.read_csv(io.StringIO(content))
            df.to_csv(safe_path, index=False)

        else:
            return "ERROR: Only .txt and .csv supported"

        logger.info(f"Wrote file: {safe_path}")
        return f"SUCCESS: Written to {file_path}"

    except Exception as e:
        logger.error(str(e))
        return f"ERROR: {str(e)}"


read_tool = FunctionTool(
    read_file,
    description="Read CSV or text files from src folder"
)

write_tool = FunctionTool(
    write_file,
    description="Write content into CSV or text files in src folder"
)

file_agent = AssistantAgent(
    name="FileAgent",
    tools=[read_tool, write_tool],
    model_client=model_client,
    system_message=(
        "You are a file processing agent.\n"
        "All files are inside 'src/' folder.\n"
        "Read only .csv and .txt files.\n"
        "Write only .txt or .csv files.\n"
    )
)