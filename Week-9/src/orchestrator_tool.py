import json
import re
import logging
from typing import Dict, List
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent

from config import model_client
from tools.code_executor import code_agent, executor
from tools.db_agent import db_agent
from tools.file_agent import file_agent
from agents.summarizer_agent import summarizer_agent

logger = logging.getLogger(__name__)


# ── Data models ───────────────────────────────────────────────
class PlanStep(BaseModel):
    agent: str
    task: str
    input_keys: List[str] = []
    output_key: str


class ExecutionPlan(BaseModel):
    steps: List[PlanStep]


# ── Orchestrator system prompt ────────────────────────────────
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
3. code  → pandas analysis only. Always needs input_keys from a previous step.

ROUTING:
- "convert X.csv to X.db"         → db (csv_to_db)
- "convert and query"              → db (csv_to_db) → db (execute_sql)
- "read and analyze"               → file (read) → code (analyze)
- "read, analyze and save"         → file (read) → code (analyze) → file (write)

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

ABSOLUTE RULES:
- db steps ALWAYS have input_keys=[]
- code ALWAYS has input_keys from a previous step
- file read ALWAYS has input_keys=[]
- ONE code step only
- Steps ordered by dependency
'''


# ── Safety guardrail ──────────────────────────────────────────
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


# ── Agents ────────────────────────────────────────────────────
orchestrator = AssistantAgent(
    name="ORCHESTRATOR",
    model_client=model_client,
    system_message=sys_msg
)


# ── Main orchestration ────────────────────────────────────────
async def run_orchestration(user_query: str) -> Dict[str, any]:

    # Safety check before hitting any agent
    safety_msg = check_query_safety(user_query)
    if safety_msg:
        print(f"\n{safety_msg}\n")
        return {"blocked": safety_msg}

    await executor.start()

    # Step 1: Generate plan
    try:
        plan_result = await orchestrator.run(task=user_query)
        plan_json = plan_result.messages[-1].content
        plan_json = re.sub(r"```(?:json)?", "", plan_json).strip().strip("`").strip()
        logger.info(f"Plan generated:\n{plan_json}")
        print(f"\nPlan:\n{plan_json}\n")
    except Exception as e:
        logger.error(f"Orchestrator failed: {e}")
        await executor.stop()
        return {"error": f"Plan generation failed: {str(e)}"}

    # Step 2: Parse plan
    try:
        plan = ExecutionPlan.model_validate(json.loads(plan_json))
    except Exception as e:
        logger.error(f"Plan parsing failed: {e}")
        await executor.stop()
        return {"error": f"Plan parsing failed: {str(e)}"}

    context: Dict[str, any] = {}

    # Step 3: Execute steps sequentially
    for i, step in enumerate(plan.steps, 1):
        print(f"[Step {i}] {step.agent.upper()}: {step.task[:60]}...")
        logger.info(f"Step {i} | Agent: {step.agent} | Task: {step.task}")

        # Inject context from previous steps
        enriched_task = step.task
        if step.input_keys:
            enriched_task += "\n\nContext from Previous Steps:\n"
            for key in step.input_keys:
                if key in context:
                    enriched_task += f"\n{key}:\n{context[key]}\n"
                else:
                    logger.warning(f"Step {i}: expected key '{key}' not found in context")

        # Run the agent
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
            if isinstance(output, str) and (output.startswith("ERROR") or output.startswith("BLOCKED")):
                logger.warning(f"Step {i} returned: {output[:100]}")
            else:
                logger.info(f"Step {i} completed. Preview: {str(output)[:80]}")

        except Exception as e:
            logger.error(f"Step {i} failed: {str(e)}", exc_info=True)
            output = f"ERROR: {str(e)}"

        context[step.output_key] = output
        print(f"Result saved to '{step.output_key}'\n")

    await executor.stop()
    return context


# ── Summarizer ────────────────────────────────────────────────
async def summarize_results(context: Dict[str, any]) -> str:
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
        return result.messages[-1].content
    except Exception as e:
        logger.error(f"Summarizer failed: {e}")
        return f"Summary failed: {str(e)}"