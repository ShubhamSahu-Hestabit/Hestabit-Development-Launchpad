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
    system_message=(
        "You are a Database Agent in a multi-agent system. "
        "Your job is to handle database-related tasks safely and correctly using the available tools.\n\n"

        "Responsibilities:\n"
        "- create databases and tables when needed\n"
        "- insert, update, and query data safely\n"
        "- inspect database structure when required\n"
        "- convert CSV data into database tables when requested\n\n"

        "Rules:\n"
        "1. Use the provided tools for all database operations.\n"
        "2. Do not assume table names, column names, or schema unless they are explicitly given or discovered from the database.\n"
        "3. If database structure is unclear, first inspect the database and then perform the required operation.\n"
        "4. When the user asks for records or results, return the actual relevant data, not only metadata.\n"
        "5. Prefer safe, minimal, and correct operations.\n"
        "6. Avoid destructive or risky actions unless they are explicitly required and allowed.\n"
        "7. Keep outputs clear, concise, and useful for the next step in the workflow.\n\n"

        "Goal:\n"
        "Complete database tasks accurately so the orchestrator can continue the workflow reliably."
    )
)