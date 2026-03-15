from dataclasses import dataclass
from typing import List, Dict


@dataclass
class UserTask:
    task: str


@dataclass
class TaskPlan:
    original_task: str
    subtasks: List[str]
    execution_graph: Dict[str, List[str]]


@dataclass
class WorkerTask:
    task: str
    subtask_id: str
    previous_results: List[str]


@dataclass
class WorkerResult:
    subtask_id: str
    result: str
    agent_id: str


@dataclass
class ReflectionTask:
    original_task: str
    worker_results: List[WorkerResult]


@dataclass
class ReflectionResult:
    refined_result: str


@dataclass
class ValidationTask:
    original_task: str
    reflected_result: str


@dataclass
class ValidationResult:
    is_valid: bool
    final_result: str


@dataclass
class FinalAnswer:
    result: str
    validation_status: bool