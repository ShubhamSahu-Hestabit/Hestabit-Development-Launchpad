import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from autogen_agentchat.agents import AssistantAgent
from config import model_client

FACT_EXTRACTION_PROMPT = """You are a fact extraction agent. Extract NEW important information ONLY from the CURRENT user message.
DO NOT extract information that is:
- Just being repeated from context
- Already mentioned earlier
- Just the agent greeting the user

Extract TWO TYPES:
1. USER FACTS (about the PERSON) - prefix with [USER]:
   - Personal info: name, age, location, occupation
   - Preferences: likes/dislikes
   - Interests, skills, goals
   ONLY extract if user EXPLICITLY STATES IT in THIS message for the FIRST TIME.

2. CONVERSATION CONTEXT (about THIS discussion) - prefix with [CONTEXT]:
   - NEW question user asked
   - NEW topic discussed

CRITICAL RULES:
- Extract ONLY from the CURRENT user message
- Do NOT extract greetings or acknowledgments
- If nothing NEW: "- No new facts"

Example 1:
User: "My name is ABC and I live in India"
Output:
- [USER] Name is ABC
- [USER] Lives in India

Example 2:
User: "What is machine learning?"
Output:
- [CONTEXT] Asked about machine learning

Example 3:
User: "What is my name?"
Output:
- No new facts"""


fact_extractor = AssistantAgent(
    name="FactExtractor",
    model_client=model_client,
    system_message=FACT_EXTRACTION_PROMPT
)
existing_user_facts = set()
async def extract_facts(user_message: str, assistant_response: str) -> dict:
    conversation = (
        f"User: {user_message}\n"
        f"Assistant: {assistant_response}\n"
        f"Extract ONLY NEW facts from the user's message above."
    )
    result = await fact_extractor.run(task=f"Extract facts from:\n{conversation}")
    facts_text = result.messages[-1].content
    user_facts = []
    context_facts = []
    for line in facts_text.strip().split('\n'):
        line = line.strip()
        if not line or not line.startswith('-'):
            continue
        if 'no new facts' in line.lower():
            continue
        if '[USER]' in line:
            fact = line.split('[USER]', 1)[1].strip()
            fact_normalized = fact.lower().replace(' ', '')
            if fact_normalized not in existing_user_facts:
                user_facts.append(fact)
                existing_user_facts.add(fact_normalized)
        elif '[CONTEXT]' in line:
            fact = line.split('[CONTEXT]', 1)[1].strip()
            context_facts.append(fact)
    return {"user_facts": user_facts, "context_facts": context_facts}