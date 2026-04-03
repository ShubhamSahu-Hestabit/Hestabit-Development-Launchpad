import asyncio
import sys
import threading
import time
from autogen_core import AgentId, SingleThreadedAgentRuntime
from agents.reflection_agent import ReflectionAgent
from agents.validator import ValidatorAgent
from agents.worker_agent import WorkerAgent
from logger_config import setup_logger
from orchestrator.messages import UserTask
from orchestrator.planner import PlannerAgent
logger = setup_logger()
stop_animation = False

def thinking_animation():
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while not stop_animation:
        sys.stdout.write("\rAgents thinking " + symbols[i % 4])
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1
async def main():
    logger.info("Day-2 system started")
    print("\nMulti-Agent Orchestration System\n")
    runtime = SingleThreadedAgentRuntime()
    await WorkerAgent.register(runtime, "worker", lambda: WorkerAgent())
    await ReflectionAgent.register(runtime, "reflection", lambda: ReflectionAgent())
    await ValidatorAgent.register(runtime, "validator", lambda: ValidatorAgent())
    await PlannerAgent.register(runtime, "planner", lambda: PlannerAgent())
    runtime.start()
    task = input("Enter your task: ").strip()
    if not task:
        print("Invalid task.")
        await runtime.stop_when_idle()
        return
    print("\nProcessing...\n")
    global stop_animation
    stop_animation = False
    spinner = threading.Thread(target=thinking_animation)
    spinner.start()
    try:
        result = await runtime.send_message(
            UserTask(task=task),
            AgentId("planner", "default")
        )
    finally:
        stop_animation = True
        spinner.join()
    print("\rDone.\n")
    print("Final Result")
    print("-" * 40)
    print(result.result)
    print("\nValidation:", "PASS" if result.validation_status else "FAIL")

    logger.info(f"Validation: {'PASS' if result.validation_status else 'FAIL'}")
    await runtime.stop_when_idle()
    logger.info("Runtime stopped")
if __name__ == "__main__":
    asyncio.run(main())