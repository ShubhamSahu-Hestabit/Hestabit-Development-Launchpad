import asyncio
from typing import List

from autogen_core import RoutedAgent, MessageContext, message_handler, AgentId
from autogen_core.models import SystemMessage, UserMessage

from orchestrator.messages import *
from config import model_client


class PlannerAgent(RoutedAgent):

    def __init__(self, num_workers: int = 3):
        super().__init__(description="Planner/Orchestrator Agent")
        self._model_client = model_client
        self._num_workers = num_workers

    @message_handler
    async def handle_task(self, message: UserTask, ctx: MessageContext) -> FinalAnswer:

        print("\n" + "#" * 80)
        print("PLANNER STARTED")
        print(f"Task: {message.task}")
        print("#" * 80 + "\n")

        # Step 1: Create plan
        task_plan = await self._plan_task(message.task)

        print("Generated Subtasks:\n")
        for i, subtask in enumerate(task_plan.subtasks):
            print(f" Worker {i}: {subtask}")
        print()

        # Step 2: Execute workers
        worker_results = await self._execute_workers(task_plan)

        # Step 3: Reflection
        reflection_result = await self._execute_reflection(
            message.task, worker_results
        )

        # Step 4: Validation
        validation_result = await self._execute_validation(
            message.task, reflection_result.refined_result
        )

        print("\nEXECUTION TREE")
        print("User")
        print(" └── Planner")
        print("      ├── Worker 1")
        print("      ├── Worker 2")
        print("      ├── Worker 3")
        print("      └── Reflection")
        print("            └── Validator")

        print("\nFINAL RESULT READY\n")

        return FinalAnswer(
            result=validation_result.final_result,
            validation_status=validation_result.is_valid,
        )

    # ---------------------------------------------------
    # PLANNING
    # ---------------------------------------------------

    async def _plan_task(self, task: str) -> TaskPlan:

        system_prompt = (
            "You are a planning agent.\n"
            "Break the user's task into 3 independent subtasks.\n"
            "Each subtask should be clear and actionable.\n\n"
            "Output format strictly as:\n"
            "SUBTASK_1: <description>\n"
            "SUBTASK_2: <description>\n"
            "SUBTASK_3: <description>\n"
        )

        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=task, source="user"),
        ]

        model_result = await self._model_client.create(messages)

        subtasks = self._parse_subtasks(str(model_result.content))

        # fallback if formatting fails
        if not subtasks:
            subtasks = [
                f"Analyze the task: {task}",
                f"Generate useful information for: {task}",
                f"Provide a structured solution for: {task}",
            ]

        execution_graph = {
            "layer_0": [f"subtask_{i}" for i in range(len(subtasks))],
            "layer_1": ["reflector"],
            "layer_2": ["validator"],
        }

        return TaskPlan(
            original_task=task,
            subtasks=subtasks,
            execution_graph=execution_graph,
        )

    # ---------------------------------------------------
    # SUBTASK PARSER
    # ---------------------------------------------------

    def _parse_subtasks(self, text: str) -> List[str]:

        subtasks = []

        for line in text.split("\n"):

            line = line.strip()

            if not line:
                continue

            if "SUBTASK_" in line and ":" in line:
                subtasks.append(line.split(":", 1)[1].strip())

            elif line[0].isdigit() and "." in line:
                subtasks.append(line.split(".", 1)[1].strip())

        return subtasks[: self._num_workers]

    # ---------------------------------------------------
    # WORKERS
    # ---------------------------------------------------

    async def _execute_workers(self, task_plan: TaskPlan):

        worker_ids = [
            AgentId("worker", f"{self.id.key}/worker_{i}")
            for i in range(len(task_plan.subtasks))
        ]

        # IMPORTANT FIX → send main task context to workers
        worker_tasks = [
            WorkerTask(
                task=f"""
MAIN TASK:
{task_plan.original_task}

SUBTASK:
{subtask}
""",
                subtask_id=f"subtask_{i}",
                previous_results=[]
            )
            for i, subtask in enumerate(task_plan.subtasks)
        ]

        results = await asyncio.gather(
            *[
                self.send_message(task, wid)
                for task, wid in zip(worker_tasks, worker_ids)
            ]
        )

        return results

    # ---------------------------------------------------
    # REFLECTION
    # ---------------------------------------------------

    async def _execute_reflection(self, task, results):

        print("\nREFLECTION AGENT STARTED\n")

        reflection_id = AgentId("reflection", f"{self.id.key}/reflection")

        reflection_task = ReflectionTask(
            original_task=task,
            worker_results=results,
        )

        return await self.send_message(reflection_task, reflection_id)

    # ---------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------

    async def _execute_validation(self, task, result):

        print("\nVALIDATOR AGENT STARTED\n")

        validator_id = AgentId("validator", f"{self.id.key}/validator")

        validation_task = ValidationTask(
            original_task=task,
            reflected_result=result,
        )

        return await self.send_message(validation_task, validator_id)