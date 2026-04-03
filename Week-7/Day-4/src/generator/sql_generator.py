# generator/sql_generator.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-70b-8192")

# Groq OpenAI-compatible client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def clean_sql_response(sql_text):
    """
    Removes markdown formatting if model returns ```sql blocks.
    """
    sql_text = sql_text.strip()

    if "```" in sql_text:
        sql_text = sql_text.split("```")[1]

    return sql_text.strip()


def generate_sql(question, schema_prompt):
    """
    Generate SELECT-only SQL using Groq LLaMA.
    """

    system_prompt = f"""
You are an expert SQLite data analyst working on a product inventory database.

STRICT RULES:
- Generate ONLY valid SQLite SELECT statements.
- NEVER use INSERT, UPDATE, DELETE, DROP, ALTER.
- Do NOT explain anything.
- Do NOT wrap SQL in markdown.
- Use only provided tables and columns.
- Use GROUP BY when aggregation is needed.
- Use ORDER BY when sorting is required.
- Use LIMIT when returning top results.

{schema_prompt}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    sql_query = response.choices[0].message.content.strip()

    return clean_sql_response(sql_query)


def summarize_result(question, columns, rows):
    """
    Convert SQL result into business summary.
    """

    result_text = "SQL RESULT:\n\n"
    result_text += "Columns: " + ", ".join(columns) + "\n\n"

    for row in rows[:20]:
        result_text += str(row) + "\n"

    summary_prompt = f"""
You are a senior business analyst.

User Question:
{question}

{result_text}

Provide a concise business insight.
Do not mention SQL.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional business analyst."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()