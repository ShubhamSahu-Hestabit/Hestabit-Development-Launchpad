import json
import logging
from autogen_core.memory import MemoryContent, MemoryMimeType

logger = logging.getLogger(__name__)

class MemoryEnabledOrchestrator:
    def __init__(self, planner_agent, agents_dict, memory_system=None):
        self.planner = planner_agent
        self.agents  = agents_dict
        self.memory  = memory_system

    def _truncate(self, content: str, max_length: int = 200) -> str:
        return content[:max_length] + "..." if len(content) > max_length else content

    async def execute(self, user_goal: str) -> str:
        logger.info(f"Starting execution: {user_goal}")
        print(f"\nGoal: {user_goal}")
        print("=" * 60)

        # 1. Fetch memory specifically for the PLANNER
        planner_context = ""
        if self.memory:
            try:
                # Use a broader query for the planner
                planner_context = await self._build_memory_context(user_goal)
            except Exception as e:
                logger.warning(f"Planner memory context failed: {e}")

        # Planning
        print("\n[Planning...]")
        plan_input = self._format_planner_input(user_goal, planner_context)

        try:
            plan_response = await self.planner.run(plan_input)
            plan = self._parse_plan(plan_response)
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return f"Planning failed: {str(e)}"

        steps = plan.get("steps", [])
        logger.info(f"Plan: {len(steps)} steps")
        print(f"  → {len(steps)} steps created\n")
        for i, step in enumerate(steps, 1):
            print(f"  {i:02d}. [{step['agent']}] {step['task'][:80]}")
        print()

        # Save goal to memory immediately
        if self.memory:
            await self._save_to_memory(f"User goal: {user_goal}", importance=6)

        # Execution
        print("[Executing...]\n")
        results = []

        for i, step in enumerate(steps, 1):
            agent_name = step.get("agent")
            task       = step.get("task")

            print(f"{'─' * 60}")
            print(f"  [{i}/{len(steps)}] {agent_name}")
            print(f"  Task: {task[:100]}")
            print(f"{'─' * 60}")
            logger.info(f"Step {i}: {agent_name}")

            if agent_name not in self.agents:
                logger.warning(f"Agent '{agent_name}' not found")
                print(f"  SKIPPED — agent not found\n")
                continue

            # 2. Fetch memory specifically for THIS task to avoid leaks
            step_memory_context = ""
            if self.memory:
                step_memory_context = await self._build_memory_context(task)

            context = self._build_agent_context(
                task, results, user_goal, step_memory_context
            )

            try:
                result = await self.agents[agent_name].run(context)
                logger.info(f"Step {i} done: {len(result)} chars")

                print(f"\n  Output ({len(result):,} chars):")
                print(f"  {'·' * 56}")
                for line in result.split('\n'):
                    print(f"  {line}")
                print(f"  {'·' * 56}\n")

                results.append({
                    "agent":  agent_name,
                    "task":   task,
                    "output": result
                })

                if self.memory and agent_name in ["Researcher", "Analyst", "Coder", "Reporter"]:
                    await self._save_to_memory(
                        f"{agent_name} output for '{task[:50]}': {self._truncate(result, 300)}",
                        importance=6
                    )

            except Exception as e:
                logger.error(f"Step {i} ({agent_name}) failed: {e}", exc_info=True)
                print(f"  ERROR: {str(e)}\n")
                results.append({
                    "agent":  agent_name,
                    "task":   task,
                    "output": f"ERROR: {str(e)}"
                })

        print("=" * 60)
        print("  All steps complete")
        print("=" * 60)

        final = self._compile_results(results)

        if self.memory:
            await self._save_to_memory(
                f"Completed goal: {user_goal}. Final Result: {self._truncate(final, 200)}",
                importance=7,
                memory_type="semantic"
            )

        return final

    async def _build_memory_context(self, query: str) -> str:
        """HYBRID: Pulls semantic facts + last 2 session items for meta-awareness."""
        parts = []
        try:
            # 1. Semantic (Vector/SQLite): For long-term relevance
            similar = await self.memory.vector.query(query)
            if similar:
                parts.append("=== RELEVANT PAST KNOWLEDGE ===\n" +
                    "\n".join(f" • {self._truncate(m.content, 300)}" for m in similar[:2]))

            # 2. Session (Episodic): For 'What did I just say?' awareness
            recent = self.memory.session.get_recent(n=2)
            if recent:
                parts.append("\n=== RECENT CONVERSATION LOGS ===\n" +
                    "\n".join(f" • {self._truncate(m.content, 200)}" for m in recent))
                    
        except Exception as e:
            logger.warning(f"Memory context failed: {e}")
        return "\n".join(parts)

    def _format_planner_input(self, user_goal: str, memory_context: str) -> str:
        if not memory_context:
            return user_goal
        return f"=== CONTEXT HISTORY ===\n{memory_context}\n\n=== USER REQUEST ===\n{user_goal}"

    def _build_agent_context(self, task, previous_results, original_goal, memory_context) -> str:
        parts = []
        if memory_context:
            parts.append("=== BACKGROUND (Check history before web search) ===\n" + memory_context)
        
        parts.append(f"\n=== ORIGINAL GOAL ===\n{self._truncate(original_goal, 150)}")
        parts.append(f"\n=== YOUR TASK ===\n{self._truncate(task, 250)}")
        
        if previous_results:
            last = previous_results[-1]
            parts.append(
                f"\n=== PREVIOUS STEP ({last['agent']}) ===\n"
                f"{self._truncate(last['output'], 1000)}"
            )
        return "\n".join(parts)

    async def _save_to_memory(self, content: str, importance: int = 5, memory_type: str = "episodic"):
        if not self.memory:
            return
        try:
            await self.memory.add(
                MemoryContent(
                    content=self._truncate(content, 600),
                    mime_type=MemoryMimeType.TEXT,
                    metadata={"importance": importance, "type": memory_type}
                ),
                store_long_term=True
            )
        except Exception as e:
            logger.warning(f"Memory save failed: {e}")

    def _parse_plan(self, plan_response: str) -> dict:
        try:
            return json.loads(plan_response)
        except json.JSONDecodeError:
            start = plan_response.find("{")
            end   = plan_response.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(plan_response[start:end])
            raise ValueError(f"Could not parse plan: {plan_response[:200]}")

    def _compile_results(self, results: list) -> str:
        if not results:
            return "No results generated."
        for r in reversed(results):
            if r["agent"] == "Reporter" and not r["output"].startswith("ERROR"):
                return r["output"]
        return results[-1]["output"]

    async def get_memory_stats(self) -> dict:
        if not self.memory:
            return {"status": "No memory system"}
        return self.memory.get_memory_stats()