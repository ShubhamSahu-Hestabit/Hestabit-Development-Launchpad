import asyncio
import os
import sys
import logging
import warnings
import traceback

warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import io
_stderr = sys.stderr
sys.stderr = io.StringIO()
from config import model_client, ACTIVE_MODEL
sys.stderr = _stderr
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
async def main():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("vectorstore", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    print("=" * 60)
    print("  NEXUS AI — Autonomous Multi-Agent System")
    print(f"  Model  : {ACTIVE_MODEL}")
    print("  Tools  : Web Search | Code Execution | File Read/Write")
    print("=" * 60)
    planner = PlannerAgent(model_client)
    coder   = CoderAgent(model_client)
    agents = {
        "Researcher": ResearcherAgent(model_client),
        "Analyst":    AnalystAgent(model_client),
        "Coder":      coder,
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
    await coder.start()
    print("\n  Commands: any task | 'stats' | 'quit'")
    print("-" * 60 + "\n")
    while True:
        try:
            task = input("Task: ").strip()
        except EOFError:
            break
        if not task:
            continue
        if task.lower() == "quit":
            await coder.stop()
            await memory_system.close()
            print("\nGoodbye!")
            break
        if task.lower() == "stats":
            stats = await orchestrator.get_memory_stats()
            print(f"\n  Session  : {stats['session']} turns")
            print(f"  Vector   : {stats['vector']} embeddings")
            print(f"  LongTerm : {stats['long_term']['total']} entries\n")
            continue
        try:
            logger.info(f"New task: {task}")
            result = await orchestrator.execute(task)
            print("\n" + "=" * 60)
            print("  FINAL RESULT")
            print("=" * 60 + "\n")
            print(result)
            print()
        except Exception as e:
            logger.error(f"Task failed: {e}", exc_info=True)
            print(f"\nERROR: {e}\n")
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())