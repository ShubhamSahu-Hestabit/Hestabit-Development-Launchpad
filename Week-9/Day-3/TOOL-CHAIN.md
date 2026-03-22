# TOOL-CHAIN.md — Day 3: Tool-Calling Agents

---

## What Is This?

A multi-agent system where a user types a natural language query, the Orchestrator breaks it into steps, and specialized agents execute each step using real tools. All steps run **sequentially** — each step passes its output to the next via a shared context.

---

## Architecture

```
User Query
     |
     v
Orchestrator
(LLM creates a JSON plan)
     |
     v
+---------+---------+---------+
|         |         |         |
File     DB       Code
Agent   Agent    Agent
|         |         |
+---------+---------+
          |
     Shared Context
    (step outputs stored
     as key-value pairs)
          |
          v
      Summarizer
          |
          v
     Final Answer
```

---

## Agents and Tools

| Agent | Tool | Responsibility | Blocked |
|-------|------|----------------|---------|
| File Agent | `read_file`, `write_file` | Reads/writes `.csv` and `.txt` only | Any other file type → `UNSUPPORTED` |
| DB Agent | `csv_to_db`, `execute_sql` | Converts CSV to SQLite, runs SELECT/INSERT | `DROP`, `DELETE`, `TRUNCATE`, `ALTER` → `BLOCKED` |
| Code Agent | `PythonCodeExecutionTool` | Runs pandas analysis on data from context | Cannot read files or save to disk |
| Summarizer | None (LLM only) | Wraps all outputs into one clean paragraph | — |

---

## Example — Full Pipeline

**Query:**
```
Read sales.csv, generate top 5 insights, write them to output.txt
```

**Orchestrator creates this plan:**
```json
{
  "steps": [
    {"agent":"file", "task":"Read sales.csv",                       "input_keys":[],           "output_key":"csv_data"},
    {"agent":"code", "task":"Generate top 5 insights using pandas", "input_keys":["csv_data"], "output_key":"insights"},
    {"agent":"file", "task":"Write insights to output.txt",         "input_keys":["insights"], "output_key":"write_result"}
  ]
}
```

**Step-by-step execution:**
```
Step 1 — File Agent
  reads sales.csv from disk
  saves content → context["csv_data"]

Step 2 — Code Agent
  receives context["csv_data"]
  runs pandas analysis
  saves result → context["insights"]

Step 3 — File Agent
  receives context["insights"]
  writes to output.txt on disk
  saves status → context["write_result"]

Summarizer
  reads all context values
  returns one final paragraph
```

---

## How to Run

```bash
# 1. Set your Groq API key (free at console.groq.com)
cd Week-9/src
echo "GROQ_API_KEY=your_key_here" > .env

# 2. Run
python main_day3.py
```

**Try this query to test the full pipeline:**
```
Read sales.csv, generate top 5 insights, write them to output.txt
```

**Try this to test the DB pipeline:**
```
Convert sales.csv to sales.db and show total revenue by region
```

---

## Project Structure

```
src/
├── main_day3.py              ← Entry point
├── orchestrator_tool.py      ← Plan generation + step execution
├── config.py                 ← Groq (primary) / Ollama (fallback)
├── tools/
│   ├── file_agent.py         ← Read/write .csv and .txt
│   ├── db_agent.py           ← SQLite + SQL queries
│   └── code_executor.py      ← Python/pandas execution
├── agents/
│   └── summarizer_agent.py   ← Final answer generation
└── src/
    └── sales.csv             ← Sample data
```