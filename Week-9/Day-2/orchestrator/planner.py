import asyncio
import re
from collections import defaultdict, deque
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core.models import SystemMessage, UserMessage
from config import model_client
from logger_config import setup_logger
from orchestrator.messages import (FinalAnswer,ReflectionTask,TaskPlan,UserTask,ValidationTask,WorkerTask,)
logger = setup_logger()
class PlannerAgent(RoutedAgent):
    def __init__(self):
        super().__init__(description="Planner / Orchestrator Agent")
        self._model_client = model_client
    @message_handler
    async def handle_task(self, message: UserTask, ctx: MessageContext) -> FinalAnswer:
        logger.info("Planner started")
        plan = await self._create_plan(message.task)
        logger.info(f"Planner generated {len(plan.subtasks)} subtasks")
        self._print_plan(plan)
        results = await self._execute_tasks(message.task, plan)
        reflection = await self.send_message(
            ReflectionTask(
                original_task=message.task,
                worker_results=results,
            ),
            AgentId("reflection", "default"),
        )
        validation = await self.send_message(
            ValidationTask(
                original_task=message.task,
                reflected_result=reflection.refined_result,
            ),
            AgentId("validator", "default"),
        )
        logger.info("Planner pipeline completed")
        return FinalAnswer(
            result=validation.final_result,
            validation_status=validation.is_valid,
        )
    async def _create_plan(self, task: str) -> TaskPlan:
        system_prompt = """
You are a Planner Agent in a multi-agent orchestration system.
Your job:
Break the user's request into clear, meaningful, non-overlapping subtasks for worker agents.
Planning rules:
- Preserve all original user requirements and constraints
- Identify hard constraints such as budget, limit, duration, quantity, deadline, or scope
- If the task has important global constraints, ensure the subtasks are designed so those constraints remain shared across the full solution
- Create only useful subtasks
- Prefer independent subtasks where possible so they can run in parallel
- Add dependencies only when a task truly needs another task's output
- Do NOT assume task numbering means execution order
- Do NOT create unnecessary chains
- Do NOT create overlapping or repetitive subtasks
- If the task is simple, return fewer subtasks
- If the task is complex, return more subtasks
- If feasibility is uncertain, include a subtask that evaluates feasibility before detailed planning
Return output in EXACTLY this format:
TASKS:
task_1: <one line task>
task_2: <one line task>
DEPENDENCIES:
task_1: none
task_2: task_1
Rules:
- Each task must be exactly one line
- Task IDs must be task_1, task_2, task_3, ...
- If a task has no dependency, write "none"
- If a task depends on others, list only the required task IDs separated by commas
- Do NOT write explanations, notes, or extra text outside this format
"""
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=task, source="user"),
        ]
        result = await self._model_client.create(messages)
        return self._parse_plan(str(result.content), task)
    def _parse_plan(self, text: str, original_task: str) -> TaskPlan:
        subtasks = {}
        dependencies = {}
        section = None
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.upper() == "TASKS:":
                section = "tasks"
                continue
            if line.upper() == "DEPENDENCIES:":
                section = "deps"
                continue
            match = re.match(r"^(task_\d+)\s*:\s*(.+)$", line, re.I)
            if not match:
                continue
            task_id = match.group(1).lower()
            value = match.group(2).strip()
            if section == "tasks":
                subtasks[task_id] = value
            elif section == "deps":
                dependencies[task_id] = [] if value.lower() == "none" else [
                    dep.strip().lower()
                    for dep in value.split(",")
                    if dep.strip()
                ]
        if not subtasks:
            logger.warning("Planner fallback triggered")
            subtasks = {
                "task_1": f"Analyze the user request: {original_task}",
                "task_2": f"Identify the major constraints and components of: {original_task}",
                "task_3": f"Prepare a structured solution for: {original_task}",
            }
            dependencies = {
                "task_1": [],
                "task_2": [],
                "task_3": ["task_1", "task_2"],
            }
        cleaned_dependencies = {}
        for task_id in subtasks:
            dep_list = dependencies.get(task_id, [])
            cleaned_dependencies[task_id] = [
                dep for dep in dep_list
                if dep in subtasks and dep != task_id
            ]
        return TaskPlan(
            original_task=original_task,
            subtasks=subtasks,
            execution_graph=cleaned_dependencies,
        )
    async def _execute_tasks(self, original_task: str, plan: TaskPlan):
        graph = plan.execution_graph
        indegree = {task_id: len(deps) for task_id, deps in graph.items()}
        reverse_graph = defaultdict(list)
        for task_id, deps in graph.items():
            for dep in deps:
                reverse_graph[dep].append(task_id)

        ready = deque([task_id for task_id, degree in indegree.items() if degree == 0])
        results = {}
        while ready:
            current_layer = list(ready)
            ready.clear()
            logger.info(f"Executing layer: {current_layer}")
            print(f"\nLayer: {', '.join(current_layer)}")
            worker_calls = []
            for task_id in current_layer:
                previous_results = [
                    results[dep].result
                    for dep in graph[task_id]
                    if dep in results
                ]
                worker_task = WorkerTask(
                    task=(
                        f"MAIN TASK:\n{original_task}\n\n"
                        f"SUBTASK ID:\n{task_id}\n\n"
                        f"SUBTASK:\n{plan.subtasks[task_id]}"
                    ),
                    subtask_id=task_id,
                    previous_results=previous_results,
                )
                worker_calls.append(
                    self.send_message(worker_task, AgentId("worker", task_id))
                )
            outputs = await asyncio.gather(*worker_calls)
            for output in outputs:
                results[output.subtask_id] = output
                for next_task in reverse_graph[output.subtask_id]:
                    indegree[next_task] -= 1
                    if indegree[next_task] == 0:
                        ready.append(next_task)
        return [results[task_id] for task_id in plan.subtasks if task_id in results]
    def _print_plan(self, plan: TaskPlan) -> None:
        print("\nTask Plan")
        print("-" * 40)
        for task_id, task_text in plan.subtasks.items():
            deps = plan.execution_graph.get(task_id, [])
            dep_text = "none" if not deps else ", ".join(deps)
            print(f"{task_id}: {task_text}")
            print(f"  depends_on: {dep_text}")
        print("\nExecution Tree")
        print("-" * 40)
        print("User")
        print("└── Planner")
        layers = self._build_execution_layers(plan.execution_graph)
        for idx, layer in enumerate(layers, start=1):
            print(f"    └── Layer {idx}")
            for task_id in layer:
                deps = plan.execution_graph.get(task_id, [])
                dep_text = f" [depends on: {', '.join(deps)}]" if deps else ""
                print(f"        └── Worker ({task_id}){dep_text}")
        print("    └── Reflection")
        print("        └── Validator")
    def _build_execution_layers(self, graph):
        indegree = {task_id: len(deps) for task_id, deps in graph.items()}
        reverse_graph = defaultdict(list)
        for task_id, deps in graph.items():
            for dep in deps:
                reverse_graph[dep].append(task_id)
        ready = deque([task_id for task_id, degree in indegree.items() if degree == 0])
        layers = []
        while ready:
            current_layer = list(ready)
            ready.clear()
            layers.append(current_layer)
            for task_id in current_layer:
                for next_task in reverse_graph[task_id]:
                    indegree[next_task] -= 1
                    if indegree[next_task] == 0:
                        ready.append(next_task)
        return layers