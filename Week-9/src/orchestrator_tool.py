import json
import re
import logging
from typing import Dict, List, Any
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from config import model_client
from tools.code_executor import run_code_task, executor
from tools.db_agent import db_agent
from tools.file_agent import file_agent
from agents.summarizer_agent import summarizer_agent

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
2. db    → csv_to_db and execute_sql. ALWAYS input_keys=[].
3. code  → supports BOTH:
   - pandas/data analysis
   - standalone Python code generation/execution
   code may have input_keys=[] for direct coding tasks.
ROUTING:
- "convert X.csv to X.db"         → db (csv_to_db)
- "convert and query"             → db (csv_to_db) → db (execute_sql)
- "read and analyze"              → file (read) → code (analyze)
- "read, analyze and save"        → file (read) → code (analyze) → file (write)
- "write code", "python program", "palindrome code", "generate program"
                                  → ONE code step directly with input_keys=[]
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
    {"agent":"code","task":"Generate 5 insights from csv data using pandas and print them clearly","input_keys":["csv_data"],"output_key":"insights"},
    {"agent":"file","task":"Write insights to output.txt","input_keys":["insights"],"output_key":"write_result"}
  ]
}
Input: "Write a Python program to check palindrome numbers"
Output:
{
  "steps": [
    {"agent":"code","task":"Write and run Python code to check whether numbers are palindrome. Use your own sample examples and print results clearly in the same code.","input_keys":[],"output_key":"result"}
  ]
}
ABSOLUTE RULES:
- db steps ALWAYS have input_keys=[]
- file read ALWAYS has input_keys=[]
- ONE code step only
- Steps ordered by dependency
- For direct coding tasks, return exactly ONE code step with input_keys=[]
- Include sample examples inside that same code step
- NEVER answer the user directly with code or prose
- ALWAYS return JSON matching the schema
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
def _clean_output_text(output: Any) -> str:
    if output is None:
        return ""
    if isinstance(output, list):
        parts = []
        for item in output:
            if hasattr(item, "content"):
                parts.append(str(item.content))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()
    return str(output).strip()
def _extract_json_object(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"```(?:json|python)?", "", text).strip().strip("`").strip()
    start = text.find("{")
    if start == -1:
        raise ValueError("No valid JSON found in planner output")
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
    raise ValueError("No complete JSON object found in planner output")
async def run_orchestration(user_query: str) -> Dict[str, Any]:
    safety_msg = check_query_safety(user_query)
    if safety_msg:
        print(f"\n{safety_msg}\n")
        return {"blocked": safety_msg}
    context: Dict[str, Any] = {}
    planner = AssistantAgent(
        name="ORCHESTRATOR",
        model_client=model_client,
        system_message=sys_msg
    )
    try:
        await executor.start()
        try:
            plan_result = await planner.run(task=user_query)
            raw_plan_output = plan_result.messages[-1].content
            try:
                plan_json = _extract_json_object(str(raw_plan_output))
                logger.info(f"Plan generated:\n{plan_json}")
                print(f"\nPlan:\n{plan_json}\n")
                plan = ExecutionPlan.model_validate(json.loads(plan_json))
            except Exception:
                logger.warning("Planner returned non-JSON output. Falling back to direct code execution.")
                direct_output = await run_code_task(user_query)
                context["result"] = _clean_output_text(direct_output)
                print("\nPlanner fallback used: direct code execution\n")
                print("Result saved to 'result'\n")
                return context
        except Exception as e:
            logger.error(f"Orchestrator failed: {e}", exc_info=True)
            return {"error": f"Plan generation failed: {str(e)}"}
        for i, step in enumerate(plan.steps, 1):
            print(f"[Step {i}] {step.agent.upper()}: {step.task[:60]}...")
            logger.info(f"Step {i} | Agent: {step.agent} | Task: {step.task}")
            enriched_task = step.task
            if step.input_keys:
                enriched_task += "\n\nContext from Previous Steps:\n"
                for key in step.input_keys:
                    if key in context:
                        enriched_task += f"\n{key}:\n{context[key]}\n"
                    else:
                        logger.warning(f"Step {i}: expected key '{key}' not found in context")
            try:
                if step.agent == "file":
                    result = await file_agent.run(task=enriched_task)
                    output = _clean_output_text(result.messages[-1].content)
                elif step.agent == "db":
                    result = await db_agent.run(task=enriched_task)
                    output = _clean_output_text(result.messages[-1].content)
                elif step.agent == "code":
                    output = await run_code_task(enriched_task)
                    output = _clean_output_text(output)
                else:
                    raise ValueError(f"Unknown agent: '{step.agent}'")
                if isinstance(output, str) and (output.startswith("ERROR") or output.startswith("BLOCKED")):
                    logger.warning(f"Step {i} returned: {output[:100]}")
                else:
                    logger.info(f"Step {i} completed. Preview: {str(output)[:80]}")
            except Exception as e:
                logger.error(f"Step {i} failed: {str(e)}", exc_info=True)
                output = f"ERROR: {str(e)}"
            context[step.output_key] = output
            print(f"Result saved to '{step.output_key}'\n")
        return context
    finally:
        try:
            await executor.stop()
        except Exception as e:
            logger.warning(f"Executor stop failed: {e}")
async def summarize_results(context: Dict[str, Any]) -> str:
    clean_context = {
        k: v for k, v in context.items()
        if isinstance(v, str) and not v.startswith("ERROR") and not v.startswith("BLOCKED")
    }
    if not clean_context:
        logger.warning("Nothing to summarize — all steps failed or were blocked")
        return "No results to summarize. Check agent_logs.log for details."
    raw_data = "\n\n".join(f"{k}:\n{v}" for k, v in clean_context.items())
    try:
        result = await summarizer_agent.run(
            task=f"Summarize this concisely:\n\n{raw_data}"
        )
        return _clean_output_text(result.messages[-1].content)
    except Exception as e:
        logger.error(f"Summarizer failed: {e}")
        return f"Summary failed: {str(e)}"