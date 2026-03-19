# TOOL-CHAIN.md
## Day 3 — Tool-Calling Agents

---

## Objective

A user gives a natural language query. The system creates a step-by-step plan, different agents execute tasks using real tools, and a final answer is produced from combined outputs.

---

## Architecture

```
User Query
    |
    v
Orchestrator (creates JSON plan)
    |
    v
+----------+----------+----------+
|          |          |          |
File      DB        Code
Agent    Agent     Agent
|          |          |
v          v          v
+------------------------------+
         Shared Context
+------------------------------+
              |
              v
         Summarizer
              |
              v
        Final Answer
```

---

## Agents and Roles

| Agent | File | Responsibility |
|-------|------|----------------|
| Orchestrator | `orchestrator.py` | Converts query into a structured execution plan |
| File Agent | `tools/file_agent.py` | Reads and writes `.csv` and `.txt` files |
| DB Agent | `tools/db_agent.py` | Runs SQL queries, converts CSV to SQLite |
| Code Agent | `tools/code_executor.py` | Executes Python code, generates insights |
| Summarizer | `agents/summarizer_agent.py` | Combines all outputs into a readable answer |

---

## How Tool Calling Works

The LLM does not execute tasks directly. It decides what to do, calls a tool, and the tool runs the actual logic.

```
Agent
  |
  v
Tool Call
  |
  v
Function Execution
  |
  v
Result returned to Agent
  |
  v
Output saved to Context
```

---

## Example 1 — CSV Analysis

**Query:** `Analyze sales.csv and generate top 5 insights`

**Plan:**

```json
{
  "steps": [
    {
      "agent": "file",
      "task": "Read sales.csv",
      "output_key": "csv_data"
    },
    {
      "agent": "code",
      "task": "Analyze data and generate top 5 insights",
      "input_keys": ["csv_data"],
      "output_key": "insights"
    }
  ]
}
```

**Flow:**

```
sales.csv
    |
    v
File Agent (read_file tool)
    |
    v
csv_data saved to context
    |
    v
Code Agent (receives csv_data)
    |
    v
Python analysis runs
    |
    v
insights saved to context
    |
    v
Summarizer --> Final Answer
```

---

## Example 2 — DB-Based Analysis

**Query:** `Convert sales.csv to database and show top products`

**Plan:**

```json
{
  "steps": [
    {
      "agent": "db",
      "task": "Use csv_to_db: csv_path='sales.csv', db_path='sales.db', table='sales'",
      "output_key": "db_created"
    },
    {
      "agent": "db",
      "task": "Use execute_sql: SELECT product, sales FROM sales ORDER BY sales DESC LIMIT 5",
      "output_key": "top_products"
    }
  ]
}
```

**Flow:**

```
sales.csv
    |
    v
DB Agent (csv_to_db tool)
    |
    v
sales.db created
    |
    v
DB Agent (execute_sql tool)
    |
    v
top_products saved to context
    |
    v
Summarizer --> Final Answer
```

---

## Context Passing

Each step saves its output to a shared context dictionary. The next step reads from it via `input_keys`.

```
Step 1 output --> context["csv_data"]
                        |
                        v
             Step 2 reads context["csv_data"]
                        |
                        v
             Step 2 output --> context["insights"]
```

---

## Tools Reference

| Task | Tool | Agent |
|------|------|-------|
| Read/write files | `read_file`, `write_file` | File Agent |
| Run SQL queries | `execute_sql` | DB Agent |
| CSV to SQLite | `csv_to_db` | DB Agent |
| Python execution | `PythonCodeExecutionTool` | Code Agent |

No external APIs. Fully local using Ollama + SQLite.

---

## Logging

```
[Step 1] FILE: Read sales.csv
Result saved to 'csv_data'

[Step 2] CODE: Generate insights
Result saved to 'insights'
```

---

## Known Limitations

- Planner may create unnecessary steps with ambiguous queries
- Missing files cause errors — ensure input files exist before running
- Not suitable for general questions outside the data pipeline

---

## Deliverables

- `/tools/code_executor.py`
- `/tools/db_agent.py`
- `/tools/file_agent.py`
- `TOOL-CHAIN.md`
