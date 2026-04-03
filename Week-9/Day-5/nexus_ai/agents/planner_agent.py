import logging
import json
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

logger = logging.getLogger(__name__)
class PlannerAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="Planner",
            model_client=model_client,
            system_message=("""You are the Orchestration Strategist. 
Your goal is to decompose user requests into a JSON plan while maintaining "Meta-Awareness" of the conversation history.
--- STRATEGIC PRIORITY: CONTEXT FIRST ---
Before creating steps, analyze the provided 'CONTEXT HISTORY' (Recent logs and Relevant Past):
1. INTERNAL QUERIES: If the user asks about the chat itself (e.g., "What did I just ask?", "Did we talk about X?"), do NOT use the Researcher. Route directly to the Reporter to answer using the provided logs.
2. REPETITION: If the context shows a task was already completed (e.g., code was written), do NOT tell the Coder to write it again. Route to the Optimizer to improve it or the Reporter to present it.
3. DATA CONTINUITY: If a previous agent (like Coder) generated data, ensure the next agent (like Analyst) is tasked with using that specific output.
--- AGENT ROSTER (Use EXACT names) ---
- Researcher  → ONLY for external web info/real-time facts.
- Analyst     → Interpret numbers, find trends, provide business insights.
- Coder       → Python execution, file handling, algorithmic logic.
- Critic      → Logic review, edge-case identification.
- Optimizer   → Refine existing code or logic for efficiency.
- Validator   → Check if the final output meets the user's specific constraints.
- Reporter    → Final output compiler. ALWAYS goes last.
--- OUTPUT FORMAT ---
You must output ONLY valid JSON. 
Example for "Did I ask about anagrams?":
{
  "steps": [
    {"agent": "Reporter", "task": "Check the recent conversation logs in the context and confirm if the user requested anagram code previously."}
  ]
}
Example for "Analyze the sales.csv we just loaded":
{
  "steps": [
    {"agent": "Coder", "task": "Read the existing sales.csv and compute totals/averages."},
    {"agent": "Analyst", "task": "Provide business insights based on the Coder's results."},
    {"agent": "Reporter", "task": "Compile the analysis into a final summary."}
  ]
}"""))
    async def run(self, content: str) -> str:
        logger.info(f"Planner evaluating goal: {content[:100]}")
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="user")], cancellation)        
        raw_output = response.chat_message.content
        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            if start != -1:
                json_str = raw_output[start:end]
                json.loads(json_str)
                return json_str
            else:
                raise ValueError("No JSON found")
        except Exception as e:
            logger.warning(f"Planner failed to produce valid JSON: {e}")
            return json.dumps({
                "steps": [{"agent": "Reporter", "task": "I encountered an error planning your request. Please try rephrasing."}]
            })