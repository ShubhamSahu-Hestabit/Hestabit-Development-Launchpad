import sqlite3
import pandas as pd
import logging
import os
from typing_extensions import Annotated
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from config import model_client

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(".")


def resolve_db_path(db_path: str) -> str:
    return os.path.join(BASE_DIR, db_path)


FORBIDDEN = ["DROP", "DELETE", "TRUNCATE", "ALTER"]


async def execute_sql(
    db_path: Annotated[str, "Database filename, e.g. sales.db"],
    query: Annotated[str, "SQL query to execute"]
) -> str:
    if not query.strip():
        return "ERROR: Empty query"
    query_upper = query.upper()
    if any(k in query_upper for k in FORBIDDEN):
        logger.warning(f"Blocked query: {query}")
        return "ERROR: Dangerous SQL not allowed"
    try:
        conn = sqlite3.connect(resolve_db_path(db_path))
        if query_upper.startswith("SELECT"):
            df = pd.read_sql_query(query, conn)
            result = df.to_string()
        else:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            result = f"SUCCESS: Rows affected {cursor.rowcount}"
        conn.close()
        return result
    except Exception as e:
        logger.error(str(e))
        return f"ERROR: {str(e)}"


async def csv_to_db(
    csv_path: Annotated[str, "CSV filename, e.g. sales.csv"],
    db_path: Annotated[str, "Database filename, e.g. sales.db"],
    table: Annotated[str, "Table name to create"]
) -> str:
    try:
        csv_full = os.path.join(BASE_DIR, csv_path)
        db_full = resolve_db_path(db_path)
        df = pd.read_csv(csv_full)
        conn = sqlite3.connect(db_full)
        df.to_sql(table, conn, if_exists="replace", index=False)
        conn.close()
        return f"SUCCESS: Table '{table}' created in {db_path}"
    except Exception as e:
        logger.error(str(e))
        return f"ERROR: {str(e)}"


sql_tool = FunctionTool(
    execute_sql,
    description="Execute SQL queries like SELECT, INSERT, UPDATE safely on a SQLite database"
)

csv_tool = FunctionTool(
    csv_to_db,
    description="Convert a CSV file into a SQLite database table"
)

db_agent = AssistantAgent(
    name="DBAgent",
    tools=[sql_tool, csv_tool],
    model_client=model_client,
    system_message="You handle databases safely using SQL tools."
)