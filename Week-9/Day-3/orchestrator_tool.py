import json
import re
import io
import logging
import contextlib
from typing import Dict, List, Any
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from config import model_client
from tools.code_executor import code_agent, executor
from tools.db_agent import db_agent, execute_sql, csv_to_db
from tools.file_agent import file_agent, read_file, write_file
from summarizer_agent import summarizer_agent

logger = logging.getLogger(__name__)
class PlanStep(BaseModel):
    agent: str
    task: str
    input_keys: List[str] = []
    output_key: str
class ExecutionPlan(BaseModel):
    steps: List[PlanStep]
sys_msg = '''
You are an orchestration planner.
Return ONLY valid JSON. No explanations. No markdown.
Schema:
{
  "steps": [
    {
      "agent": "file | db | code",
      "task": "string",
      "input_keys": ["string"],
      "output_key": "string"
    }
  ]
}
AGENT RULES:
1. file  → reads/writes .csv and .txt only. input_keys=[] for reads.
2. db    → csv_to_db and execute_sql. ALWAYS input_keys=[]. Never needs file agent first.
3. code  → pandas analysis only. Usually needs input_keys from a previous step, EXCEPT when generating new CSV content from scratch.

ROUTING:
- "convert X.csv to X.db"         → db (csv_to_db)
- "convert and query"             → db (csv_to_db) → db (execute_sql)
- "read and analyze"              → file (read) → code (analyze)
- "read, analyze and save"        → file (read) → code (analyze) → file (write)
- "create a csv/txt file"         → code (generate content) → file (write)
EXAMPLES:
Input: "Convert sales.csv to sales.db and show revenue by region"
Output:
{
  "steps": [
    {"agent":"db","task":"Use csv_to_db tool: csv_path='sales.csv', db_path='sales.db', table='sales'","input_keys":[],"output_key":"db_created"},
    {"agent":"db","task":"Use execute_sql tool: db_path='sales.db', query='SELECT region, SUM(revenue) as total FROM sales GROUP BY region ORDER BY total DESC'","input_keys":[],"output_key":"region_revenue"}
  ]
}
Input: "Analyze sales.csv and write insights to output.txt"
Output:
{
  "steps": [
    {"agent":"file","task":"Read sales.csv","input_keys":[],"output_key":"csv_data"},
    {"agent":"code","task":"Generate 5 insights from csv data using pandas","input_keys":["csv_data"],"output_key":"insights"},
    {"agent":"file","task":"Write insights to output.txt","input_keys":["insights"],"output_key":"write_result"}
  ]
}
Input: "Create a sales.csv with 15 entries of ecommerce products"
Output:
{
  "steps": [
    {"agent":"code","task":"Generate valid CSV data with 15 entries of ecommerce products. Output ONLY CSV format with header row using print().","input_keys":[],"output_key":"csv_data"},
    {"agent":"file","task":"Write csv_data to sales.csv","input_keys":["csv_data"],"output_key":"write_result"}
  ]
}
ABSOLUTE RULES:
- db steps ALWAYS have input_keys=[]
- file read ALWAYS have input_keys=[]
- file write uses input_keys from previous step
- ONE code step only
- Steps ordered by dependency
- For file creation requests, do NOT answer directly with file contents; return JSON plan only
'''
FORBIDDEN_INTENTS = ["drop table", "delete from", "truncate table"]
def check_query_safety(query: str) -> str | None:
    q = query.lower()
    for intent in FORBIDDEN_INTENTS:
        if intent in q:
            logger.warning(f"Blocked destructive query: {query}")
            return (
                f"BLOCKED: '{intent}' is a destructive operation and is not allowed.\n"
                f"DB Agent only supports SELECT and INSERT.\n"
                f"Try: 'Query sales.db and filter by cost < 100000'"
            )
    return None
def _extract_tool_payload(output: str, tool_name: str) -> dict | None:
    patterns = [
        rf"<{tool_name}>\s*(\{{.*?\}})\s*</{tool_name}>",
        rf"<{tool_name}>\s*(\{{.*?\}})\s*</function>",
        rf"<function={tool_name}>\s*(\{{.*?\}})"
    ]
    for pattern in patterns:
        match = re.search(pattern, output, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                return None
    return None
def _extract_code_executor_payload(output: str) -> dict | None:
    patterns = [
        r"<CodeExecutor>\s*(\{.*?\})\s*</CodeExecutor>",
        r"<CodeExecutor>\s*(\{.*\})",
        r"<function=CodeExecutor>\s*(\{.*\})"
    ]
    for pattern in patterns:
        match = re.search(pattern, output, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                continue
    return None
def _run_code_fallback(code: str) -> str:
    import pandas as pd
    stdout_buffer = io.StringIO()
    exec_globals = {
        "__builtins__": __builtins__,
        "pd": pd,
        "io": io,
    }
    with contextlib.redirect_stdout(stdout_buffer):
        exec(code, exec_globals, exec_globals)
    return stdout_buffer.getvalue().strip()
def _normalize_code_output(step: PlanStep, output: str) -> str:
    text = output.strip()
    if step.output_key == "csv_data":
        lines = [line for line in text.splitlines() if line.strip()]
        if lines:
            return "\n".join(lines).strip()
    if step.output_key == "insights":
        return text.strip()
    return text
async def _fallback_execute_tool(step: PlanStep, output: str):
    if step.agent == "file":
        payload = _extract_tool_payload(output, "write_file")
        if payload:
            return await write_file(
                file_path=payload["file_path"],
                content=payload["content"],
            )
        payload = _extract_tool_payload(output, "read_file")
        if payload:
            return await read_file(file_path=payload["file_path"])
    if step.agent == "db":
        payload = _extract_tool_payload(output, "execute_sql")
        if payload:
            return await execute_sql(
                db_path=payload["db_path"],
                query=payload["query"],
            )
        payload = _extract_tool_payload(output, "csv_to_db")
        if payload:
            return await csv_to_db(
                csv_path=payload["csv_path"],
                db_path=payload["db_path"],
                table=payload["table"],
            )
    if step.agent == "code":
        payload = _extract_code_executor_payload(output)
        if payload and "code" in payload:
            return _run_code_fallback(payload["code"])
    return output
def _preview_output(step: PlanStep, output: Any) -> str:
    text = str(output).strip()
    if step.output_key == "csv_data":
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            return "Generated empty CSV output"
        header = lines[0]
        rows = max(len(lines) - 1, 0)
        return f"Generated CSV with {rows} rows | header: {header}"
    if step.output_key == "insights":
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return "No insights generated"
        return " | ".join(lines[:5])
    if step.output_key == "write_result":
        return text
    if step.output_key == "db_created":
        return text
    return text[:200] + ("..." if len(text) > 200 else "")

def _build_enriched_task(step: PlanStep, context: Dict[str, Any]) -> str:
    if step.agent == "file" and step.task.lower().startswith("write ") and step.input_keys:
        content_key = step.input_keys[0]
        file_match = re.search(r"to\s+([^\s]+)$", step.task.strip(), re.IGNORECASE)
        file_name = file_match.group(1) if file_match else "output.txt"
        content = context.get(content_key, "")
        return f"Write this exact content to {file_name}:\n\n{content}"

    enriched_task = step.task
    if step.input_keys:
        enriched_task += "\n\nContext from Previous Steps:\n"
        for key in step.input_keys:
            if key in context:
                enriched_task += f"\n{key}:\n{context[key]}\n"
            else:
                logger.warning(f"Expected key '{key}' not found in context")

    return enriched_task
orchestrator = AssistantAgent(
    name="ORCHESTRATOR",
    model_client=model_client,
    system_message=sys_msg
)
async def run_orchestration(user_query: str) -> Dict[str, Any]:
    safety_msg = check_query_safety(user_query)
    if safety_msg:
        print(f"\n{safety_msg}\n")
        return {"blocked": safety_msg}
    await executor.start()
    try:
        plan_result = await orchestrator.run(task=user_query)
        plan_json = plan_result.messages[-1].content
        plan_json = re.sub(r"```(?:json)?", "", plan_json).strip().strip("`").strip()
        logger.info(f"Plan generated:\n{plan_json}")
        print("\nPlan:")
        print(plan_json)
    except Exception as e:
        logger.error(f"Orchestrator failed: {e}")
        await executor.stop()
        return {"error": f"Plan generation failed: {str(e)}"}
    try:
        if not plan_json.startswith("{"):
            raise ValueError("Planner did not return valid JSON")
        plan = ExecutionPlan.model_validate(json.loads(plan_json))
    except Exception as e:
        logger.error(f"Plan parsing failed: {e}")
        await executor.stop()
        return {"error": f"ERROR: Plan parsing failed: {str(e)}"}

    context: Dict[str, Any] = {}
    for i, step in enumerate(plan.steps, 1):
        print(f"\n[Step {i}/{len(plan.steps)}] {step.agent.upper()}")
        logger.info(f"Step {i} | Agent: {step.agent} | Task: {step.task}")
        enriched_task = _build_enriched_task(step, context)
        try:
            if step.agent == "file":
                result = await file_agent.run(task=enriched_task)
            elif step.agent == "db":
                result = await db_agent.run(task=enriched_task)
            elif step.agent == "code":
                result = await code_agent.run(task=enriched_task)
            else:
                raise ValueError(f"Unknown agent: '{step.agent}'")
            output = result.messages[-1].content
            if isinstance(output, str) and (
                output.startswith("<CodeExecutor>")
                or output.startswith("<function=CodeExecutor>")
            ):
                logger.warning(f"Step {i} returned pseudo CodeExecutor output. Running fallback execution.")
                output = await _fallback_execute_tool(step, output)
            if isinstance(output, str) and (
                output.startswith("<write_file>")
                or output.startswith("<read_file>")
                or output.startswith("<execute_sql>")
                or output.startswith("<csv_to_db>")
                or output.startswith("<function=write_file>")
                or output.startswith("<function=read_file>")
                or output.startswith("<function=execute_sql>")
                or output.startswith("<function=csv_to_db>")
            ):
                logger.warning(f"Step {i} returned pseudo tool call. Running fallback execution.")
                output = await _fallback_execute_tool(step, output)
            if step.agent == "code" and isinstance(output, str):
                output = _normalize_code_output(step, output)
            if isinstance(output, str) and (output.startswith("ERROR") or output.startswith("BLOCKED")):
                logger.warning(f"Step {i} returned: {output[:100]}")
                print(f"Task: {step.task}")
                print(f"Saved as: {step.output_key}")
                print(f"Outcome: {output}")
            else:
                logger.info(f"Step {i} completed. Preview: {str(output)[:80]}")
                print(f"Task: {step.task}")
                print(f"Saved as: {step.output_key}")
                print(f"Outcome: {_preview_output(step, output)}")
        except Exception as e:
            logger.error(f"Step {i} failed: {str(e)}", exc_info=True)
            output = f"ERROR: {str(e)}"
            print(f"Task: {step.task}")
            print(f"Saved as: {step.output_key}")
            print(f"Outcome: {output}")
        context[step.output_key] = output
    await executor.stop()
    return context
async def summarize_results(context: Dict[str, Any]) -> str:
    clean_context = {
        k: v for k, v in context.items()
        if isinstance(v, str)
        and not v.startswith("ERROR")
        and not v.startswith("BLOCKED")
        and "Plan parsing failed" not in v
    }
    if not clean_context:
        logger.warning("Nothing to summarize — all steps failed or were blocked")
        return "No results to summarize. Check agent_logs.log for details."
    raw_data = "\n\n".join(f"{k}:\n{v}" for k, v in clean_context.items())
    try:
        result = await summarizer_agent.run(
            task=f"Summarize this concisely:\n\n{raw_data}"
        )
        return result.messages[-1].content
    except Exception as e:
        logger.error(f"Summarizer failed: {e}")
        return f"Summary failed: {str(e)}"