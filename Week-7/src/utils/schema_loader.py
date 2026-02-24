# utils/schema_loader.py

from sqlalchemy import create_engine, inspect
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "enterprise.db")


def load_schema():
    """
    Dynamically extracts schema using SQLAlchemy Inspector.
    """
    engine = create_engine(f"sqlite:///{DB_PATH}")
    inspector = inspect(engine)

    schema = {}

    for table in inspector.get_table_names():
        columns = inspector.get_columns(table)
        schema[table] = [
            {"name": col["name"], "type": str(col["type"])}
            for col in columns
        ]

    return schema


def format_schema(schema_dict):
    """
    Formats schema into LLM-friendly text.
    """
    formatted = "DATABASE SCHEMA:\n\n"

    for table, columns in schema_dict.items():
        formatted += f"Table: {table}\n"
        for col in columns:
            formatted += f"- {col['name']} ({col['type']})\n"
        formatted += "\n"

    return formatted