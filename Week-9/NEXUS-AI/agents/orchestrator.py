import json
import logging
from autogen_core.memory import MemoryContent, MemoryMimeType

logger = logging.getLogger(__name__)


class MemoryEnabledOrchestrator:
    def __init__(self, planner_agent, agents_dict, memory_system=None):
        self.planner = planner_agent
        self.agents = agents_dict
        self.memory = memory_system

    def _truncate(self, content: str, max_length: int = 200) -> str:
        return content[:max_length] + "..." if len(content) > max_length else content

    async def execute(self, user_goal: str) -> str:
        logger.info(f"Starting execution for: {user_goal}")
        print(f"\nGoal: {user_goal}")
        print("=" * 70)

        # Build memory context
        memory_context = ""
        if self.memory:
            memory_context = await self._build_memory_context(user_goal)

        # Phase 1: Planning
        print("\nPhase 1: Planning...")
        plan_input = self._format_planner_input(user_goal, memory_context)

        try:
            plan_response = await self.planner.run(plan_input)
            plan = self._parse_plan(plan_response)
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return f"Planning failed: {str(e)}"

        steps = plan.get("steps", [])
        logger.info(f"Plan created with {len(steps)} steps")
        print(f"Plan: {len(steps)} steps\n")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step['agent']}: {self._truncate(step['task'], 80)}")

        # Save goal to memory
        if self.memory:
            await self._save_to_memory(f"User goal: {user_goal}", importance=6)

        # Phase 2: Execution
        print("\nPhase 2: Execution...\n")
        results = []

        for i, step in enumerate(steps, 1):
            agent_name = step.get("agent")
            task = step.get("task")
            print(f"[{i}/{len(steps)}] {agent_name}: {self._truncate(task, 80)}")
            logger.info(f"Step {i}: {agent_name}")

            if agent_name not in self.agents:
                logger.warning(f"Agent '{agent_name}' not found, skipping")
                print(f"  SKIPPED — agent not found\n")
                continue

            context = self._build_agent_context(task, results, user_goal, memory_context)

            try:
                agent = self.agents[agent_name]
                result = await agent.run(context)
                logger.info(f"Step {i} completed: {len(result)} chars")
                print(f"  Done ({len(result)} chars)\n")

                results.append({
                    "agent": agent_name,
                    "task": task,
                    "output": result
                })

                if self.memory and agent_name in ["Researcher", "Analyst", "Coder", "Reporter"]:
                    await self._save_to_memory(
                        f"{agent_name}: {self._truncate(result, 300)}",
                        importance=6
                    )

            except Exception as e:
                logger.error(f"Step {i} ({agent_name}) failed: {e}", exc_info=True)
                print(f"  ERROR: {str(e)}\n")
                results.append({
                    "agent": agent_name,
                    "task": task,
                    "output": f"ERROR: {str(e)}"
                })

        print("=" * 70)
        print("Execution Complete!")
        print("=" * 70)

        final = self._compile_results(results)

        if self.memory:
            await self._save_to_memory(
                f"Completed: {user_goal}. Result: {self._truncate(final, 200)}",
                importance=7,
                memory_type="semantic"
            )

        return final

    async def _build_memory_context(self, query: str) -> str:
        parts = []
        try:
            important = await self.memory.long_term.get_important_memories(min_importance=7, limit=3)
            if important:
                facts = [f" • {self._truncate(m.content, 150)}" for m in important]
                parts.append("=== IMPORTANT CONTEXT ===\n" + "\n".join(facts))

            similar = await self.memory.vector.query(query)
            if similar:
                relevant = [f" • {self._truncate(m.content, 150)}" for m in similar[:2]]
                parts.append("\n=== RELEVANT PAST ===\n" + "\n".join(relevant))

            recent = self.memory.session.get_recent(n=2)
            if recent:
                recent_items = [f" • {self._truncate(m.content, 150)}" for m in recent]
                parts.append("\n=== RECENT ===\n" + "\n".join(recent_items))
        except Exception as e:
            logger.warning(f"Memory context build failed: {e}")

        return "\n".join(parts)

    def _format_planner_input(self, user_goal: str, memory_context: str) -> str:
        if not memory_context:
            return user_goal
        return f"{self._truncate(memory_context, 500)}\n\n=== USER REQUEST ===\n{user_goal}"

    def _build_agent_context(self, task, previous_results, original_goal, memory_context) -> str:
        parts = []
        if memory_context:
            parts.append(self._truncate(memory_context, 400))
        parts.append(f"\n=== ORIGINAL GOAL ===\n{self._truncate(original_goal, 150)}")
        parts.append(f"\n=== YOUR TASK ===\n{self._truncate(task, 250)}")
        if previous_results:
            last = previous_results[-1]
            parts.append(f"\n=== PREVIOUS STEP ===\n{last['agent']}: {self._truncate(last['output'], 200)}")
        return "\n".join(parts)

    async def _save_to_memory(self, content: str, importance: int = 5, memory_type: str = "episodic"):
        if not self.memory:
            return
        try:
            memory_content = MemoryContent(
                content=self._truncate(content, 500),
                mime_type=MemoryMimeType.TEXT,
                metadata={"importance": importance, "type": memory_type}
            )
            await self.memory.add(memory_content, store_long_term=True)
        except Exception as e:
            logger.warning(f"Memory save failed: {e}")

    def _parse_plan(self, plan_response: str) -> dict:
        try:
            return json.loads(plan_response)
        except json.JSONDecodeError:
            start = plan_response.find("{")
            end = plan_response.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(plan_response[start:end])
            raise ValueError(f"Could not parse plan: {plan_response[:200]}")

    def _compile_results(self, results: list) -> str:
        if not results:
            return "No results generated."
        # Return Reporter output if available, else last agent
        for r in reversed(results):
            if r["agent"] == "Reporter" and not r["output"].startswith("ERROR"):
                return r["output"]
        return results[-1]["output"]

    async def get_memory_stats(self) -> dict:
        if not self.memory:
            return {"status": "No memory system"}
        return self.memory.get_memory_stats()