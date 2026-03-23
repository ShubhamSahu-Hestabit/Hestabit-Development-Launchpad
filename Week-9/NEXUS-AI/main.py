import asyncio
import os
import sys
import logging
import traceback
from datetime import datetime

from config import model_client
from agents.planner_agent import PlannerAgent
from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.coder_agent import CoderAgent
from agents.critic_agent import CriticAgent
from agents.optimiser_agent import OptimizerAgent
from agents.validator_agent import ValidatorAgent
from agents.reporter_agent import ReporterAgent
from agents.orchestrator import MemoryEnabledOrchestrator
from memory.agent_memory import AgentMemorySystem

logger = logging.getLogger(__name__)


class TeeOutput:
    """Writes output to both terminal and file simultaneously."""
    def __init__(self, file_path):
        self.terminal = sys.__stdout__
        self.file = open(file_path, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
        self.file.flush()

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def isatty(self):
        return self.terminal.isatty()

    def close(self):
        self.file.close()


async def main():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("vectorstore", exist_ok=True)

    # Setup agents
    planner  = PlannerAgent(model_client)
    agents = {
        "Researcher": ResearcherAgent(model_client),
        "Analyst":    AnalystAgent(model_client),
        "Coder":      CoderAgent(model_client),
        "Critic":     CriticAgent(model_client),
        "Optimizer":  OptimizerAgent(model_client),
        "Validator":  ValidatorAgent(model_client),
        "Reporter":   ReporterAgent(model_client),
    }

    memory_system = AgentMemorySystem(
        session_max_turns=50,
        vector_k=5,
        vector_threshold=0.3,
        db_path="vectorstore/agent_long_term.db",
        vector_persist_path="vectorstore/agent_vectors.faiss"
    )

    orchestrator = MemoryEnabledOrchestrator(planner, agents, memory_system)

    print("=" * 70)
    print("  NEXUS AI — Multi-Agent System")
    print("=" * 70)
    print("Type your task or 'stats' to see memory stats or 'quit' to exit\n")

    while True:
        try:
            task = input("Task: ").strip()
        except EOFError:
            break

        if not task:
            continue

        if task.lower() == "quit":
            await memory_system.close()
            print("Goodbye!")
            break

        if task.lower() == "stats":
            stats = await orchestrator.get_memory_stats()
            print(f"\nMemory Stats: {stats}\n")
            continue

        # Setup output file for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"logs/output_{timestamp}.md"
        tee = TeeOutput(output_file)
        sys.stdout = tee

        try:
            logger.info(f"New task: {task}")
            result = await orchestrator.execute(task)

            print("\n" + "=" * 70)
            print("FINAL OUTPUT")
            print("=" * 70)
            print(result)

            stats = await orchestrator.get_memory_stats()
            print(f"\nMemory Stats: {stats}")

        except Exception as e:
            logger.error(f"Task failed: {e}", exc_info=True)
            print(f"\nERROR: {e}")
            traceback.print_exc()

        finally:
            sys.stdout = sys.__stdout__
            tee.close()
            print(f"\nOutput saved to {output_file}\n")


if __name__ == "__main__":
    asyncio.run(main())