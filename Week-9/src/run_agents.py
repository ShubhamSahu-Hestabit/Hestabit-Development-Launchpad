import asyncio
import sys
import time
import threading

from autogen_core import SingleThreadedAgentRuntime, AgentId

from orchestrator.messages import UserTask
from orchestrator.planner import PlannerAgent
from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectionAgent
from agents.validator import ValidatorAgent


# -------- Thinking Animation --------
stop_animation = False

def thinking_animation():
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while not stop_animation:
        sys.stdout.write("\rAgents thinking " + symbols[i % len(symbols)])
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1


async def main():

    print("\n" + "="*80)
    print("MULTI-AGENT ORCHESTRATION SYSTEM")
    print("="*80 + "\n")

    print("Initializing runtime...\n")

    runtime = SingleThreadedAgentRuntime()

    print("Registering agents...")

    await WorkerAgent.register(
        runtime,
        "worker",
        lambda: WorkerAgent()
    )

    await ReflectionAgent.register(
        runtime,
        "reflection",
        lambda: ReflectionAgent()
    )

    await ValidatorAgent.register(
        runtime,
        "validator",
        lambda: ValidatorAgent()
    )

    await PlannerAgent.register(
        runtime,
        "planner",
        lambda: PlannerAgent(num_workers=3)
    )

    print("Registered agents: planner, worker, reflection, validator\n")

    runtime.start()

    print("Runtime started\n")

    task = input("Enter your task: ")

    print("\n" + "="*80)
    print("TASK RECEIVED")
    print("="*80)
    print(task)
    print("\nProcessing through agent pipeline...\n")

    # Start spinner
    global stop_animation
    stop_animation = False
    spinner = threading.Thread(target=thinking_animation)
    spinner.start()

    # Execute pipeline
    result = await runtime.send_message(
        UserTask(task=task),
        AgentId("planner", "default")
    )

    # Stop spinner
    stop_animation = True
    spinner.join()

    print("\rProcessing complete!                     ")

    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80 + "\n")

    print(result.result)

    print("\n" + "="*80)
    print(f"Validation Status: {'PASS' if result.validation_status else 'FAIL'}")
    print("="*80 + "\n")

    await runtime.stop_when_idle()

    print("Runtime stopped\n")


if __name__ == "__main__":
    asyncio.run(main())