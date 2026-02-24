# pipelines/sql_pipeline.py

import os
from sqlalchemy import create_engine, text
from utils.schema_loader import load_schema, format_schema
from generator.sql_generator import generate_sql, summarize_result

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "enterprise.db")


def validate_sql(sql):
    """
    Enforces SELECT-only and prevents injection.
    """
    sql_clean = sql.lower().strip()

    if not sql_clean.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    forbidden = ["insert", "update", "delete", "drop", "alter"]

    for word in forbidden:
        if word in sql_clean:
            raise ValueError("Unsafe SQL detected.")

    if ";" in sql_clean[:-1]:
        raise ValueError("Multiple statements not allowed.")

    return True


def execute_sql(sql):
    """
    Safely executes SQL using SQLAlchemy.
    """
    engine = create_engine(f"sqlite:///{DB_PATH}")

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

    return columns, rows


def run_sql_pipeline(question):
    """
    Complete pipeline: Text → SQL → Validate → Execute → Summarize
    """

    # 1. Load schema
    schema = load_schema()
    schema_prompt = format_schema(schema)

    # 2. Generate SQL
    sql_query = generate_sql(question, schema_prompt)
    print("\nGenerated SQL:\n", sql_query)

    # 3. Validate
    validate_sql(sql_query)

    # 4. Execute
    columns, rows = execute_sql(sql_query)

    if not rows:
        return "No records found."

    # 5. Summarize
    summary = summarize_result(question, columns, rows)

    return summary