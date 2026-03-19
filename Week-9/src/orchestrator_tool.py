import json
import logging
from typing import Dict, List
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient

from tools.code_executor import code_agent, executor
from tools.db_agent import db_agent
from tools.file_agent import file_agent
from agents.summarizer_agent import summarizer_agent


# Minimal logging (no separate file if you don’t want)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
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

Your job is ONLY to describe an execution plan.
You MUST return ONLY valid JSON that matches this schema exactly:

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

STRICT RULES:

1. Agent responsibilities:
   - file → READ files (CSVs, text) and WRITE files (output.txt, reports)
   - db   → Execute SQL queries (use execute_sql tool), CSV to database conversion (use csv_to_db tool)
   - code → Perform Python analysis USING data from file/db agent (NOT for CSV-to-DB conversion or read files directly)

2. All files are located inside 'src/' directory. Always refer using filename only.

3. MANDATORY EXAMPLES:

Input: "Convert sales.csv to sales.db and display table"
Output:
{
  "steps": [
    {
      "agent": "db",
      "task": "Use csv_to_db tool: csv_path='sales.csv', db_path='sales.db', table='sales'",
      "input_keys": [],
      "output_key": "db_created"
    },
    {
      "agent": "db",
      "task": "Use execute_sql tool: db_path='sales.db', query='SELECT * FROM sales'",
      "input_keys": [],
      "output_key": "table_data"
    }
  ]
}

Input: "Analyze sales.csv and write insights to output.txt"
Output:
{
  "steps": [
    {
      "agent": "file",
      "task": "Read sales.csv",
      "input_keys": [],
      "output_key": "csv_data"
    },
    {
      "agent": "code",
      "task": "Generate 5 insights from data",
      "input_keys": ["csv_data"],
      "output_key": "insights"
    },
    {
      "agent": "file",
      "task": "Write insights to output.txt",
      "input_keys": ["insights"],
      "output_key": "write_result"
    }
  ]
}

3. Code agent is STATELESS - use ONLY ONE code step between file operations

4. Steps MUST be ordered by dependency

Return ONLY raw JSON. No explanations.
'''


model_client = OllamaChatCompletionClient(
    model="qwen2.5:7b-instruct-q4_0"
)


orchestrator = AssistantAgent(
    name="ORCHESTRATOR",
    model_client=model_client,
    system_message=sys_msg
)


async def run_orchestration(user_query: str) -> Dict[str, any]:
    await executor.start()

    #  Step 1: Generate Plan
    plan_result = await orchestrator.run(task=user_query)
    plan_json = plan_result.messages[-1].content
    print(f"\nPlan:\n{plan_json}\n")

    plan = ExecutionPlan.model_validate(json.loads(plan_json))
    context: Dict[str, any] = {}

    #  Step 2: Execute Steps
    for i, step in enumerate(plan.steps, 1):
        print(f"[Step {i}] {step.agent.upper()}: {step.task[:60]}...")

        enriched_task = step.task

        # Inject context
        if step.input_keys:
            enriched_task += "\n\nContext from Previous Steps:\n"
            for key in step.input_keys:
                if key in context:
                    enriched_task += f"\n{key}:\n{context[key]}\n"

        try:
            if step.agent == "file":
                result = await file_agent.run(task=enriched_task)

                #  FIXED safe extraction
                try:
                    output = result.messages[-1].content
                except Exception:
                    output = str(result)

            elif step.agent == "db":
                result = await db_agent.run(task=enriched_task)
                output = result.messages[-1].content

            elif step.agent == "code":
                result = await code_agent.run(task=enriched_task)
                output = result.messages[-1].content

            else:
                raise ValueError(f"Unknown agent: {step.agent}")

        except Exception as e:
            logger.error(f"Step failed: {str(e)}")
            output = f"ERROR: {str(e)}"

        context[step.output_key] = output
        print(f"Result saved to '{step.output_key}'\n")

    await executor.stop()
    return context


async def summarize_results(context: Dict[str, any]) -> str:
    raw_data = "\n\n".join(f"{k}:\n{v}" for k, v in context.items())
    result = await summarizer_agent.run(
        task=f"Summarize this concisely:\n\n{raw_data}"
    )
    return result.messages[-1].content