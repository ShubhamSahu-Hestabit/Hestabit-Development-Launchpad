import os
import logging
from typing_extensions import Annotated
from autogen_core.tools import FunctionTool

logger = logging.getLogger(__name__)
BASE_DIR   = os.path.abspath(".")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
def resolve_read_path(file_name: str) -> str:
    return os.path.join(BASE_DIR, file_name)
def resolve_write_path(file_name: str) -> str:
    return os.path.join(OUTPUT_DIR, file_name)
async def read_file(
    file_path: Annotated[str, "File path relative to nexus_ai/, e.g. sales.csv"]
) -> str:
    if "." not in file_path:
        return "ERROR: Provide valid file name like data.csv"
    safe_path = resolve_read_path(file_path)
    if not os.path.exists(safe_path):
        return f"ERROR: File not found → {file_path}"
    if file_path.endswith((".csv", ".txt", ".md")):
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    return "UNSUPPORTED: Only .csv, .txt, .md supported"
async def write_file(
    file_path: Annotated[str, "File name only e.g. report.md"],
    content: Annotated[str, "Content to write"]
) -> str:
    if "." not in file_path:
        return "ERROR: Invalid file name"
    if not content or not str(content).strip():
        return "ERROR: Cannot write empty content"
    file_name = os.path.basename(file_path)
    safe_path = resolve_write_path(file_name)
    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(str(content))
        return f"SUCCESS: Written to outputs/{file_name}"
    except Exception as e:
        return f"ERROR: {str(e)}"
read_tool = FunctionTool(
    read_file,
    description="Read a .csv, .txt or .md file from nexus_ai/ folder"
)
write_tool = FunctionTool(
    write_file,
    description="Write content to a file, always saves to outputs/ folder"
)