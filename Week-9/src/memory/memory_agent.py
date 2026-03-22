from autogen_agentchat.agents import AssistantAgent
from autogen_core.memory import MemoryContent, MemoryMimeType
from unified_memory import UnifiedMemory
from fact_extractor import extract_facts, existing_user_facts


class MemoryAgent:
    """
    Wraps AssistantAgent with UnifiedMemory.
    Flow: Search → Inject → Generate → Store → Extract facts
    """

    def __init__(self, model_client):
        self.memory = UnifiedMemory()
        self.agent = AssistantAgent(
            name="MemoryAgent",
            model_client=model_client,
            memory=[self.memory],
            system_message="You are a helpful assistant with memory."
        )

        # Load existing facts into dedup tracker on startup
        existing_facts = self.memory.longterm.get_all_semantic_facts()
        for fact in existing_facts:
            existing_user_facts.add(fact.lower().replace(' ', ''))

        print(f"Loaded: {len(existing_facts)} facts, {len(self.memory.vector)} embeddings")

    async def run(self, user_input: str) -> str:
        # Step 1: Search memory
        results = await self.memory.query(user_input)

        # Step 2: Inject context if found
        enhanced_task = user_input
        if results.results:
            context = "Relevant memories:\n"
            for i, mem in enumerate(results.results[:2], 1):
                sim = mem.metadata.get('similarity', 0) if mem.metadata else 0
                context += f"{i}. {mem.content} [{sim:.2f}]\n"
            enhanced_task = f"{context}\nUser: {user_input}"

        # Step 3: Generate response
        result = await self.agent.run(task=enhanced_task)
        response = result.messages[-1].content

        # Step 4: Store conversation in session + vector
        await self.memory.session.add(
            MemoryContent(content=f"User: {user_input}", mime_type=MemoryMimeType.TEXT)
        )
        await self.memory.session.add(
            MemoryContent(content=f"Assistant: {response}", mime_type=MemoryMimeType.TEXT)
        )
        await self.memory.vector.add(
            MemoryContent(content=f"Q: {user_input}\nA: {response}", mime_type=MemoryMimeType.TEXT)
        )

        # Step 5: Extract and store facts in longterm
        print("Extracting facts...")
        facts = await extract_facts(user_input, response)

        for fact in facts["user_facts"]:
            await self.memory.add(
                MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT),
                memory_type="semantic",
                importance=9
            )
        for fact in facts["context_facts"]:
            await self.memory.add(
                MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT),
                memory_type="episodic",
                importance=5
            )

        if facts["user_facts"] or facts["context_facts"]:
            print(f"Saved: {len(facts['user_facts'])} user facts, {len(facts['context_facts'])} context facts")

        return response

    async def debug(self):
        session_result = await self.memory.session.query("")
        user_facts = await self.memory.longterm.query(memory_type="semantic", limit=10)
        context = await self.memory.longterm.query(memory_type="episodic", limit=10)

        print(f"\nSession Messages = {len(session_result.results)}:")
        for i, mem in enumerate(session_result.results, 1):
            print(f"  {i}. {mem.content[:60]}")

        print(f"\nUser Facts = {len(user_facts.results)}:")
        for i, fact in enumerate(user_facts.results, 1):
            print(f"  {i}. {fact.content}")

        print(f"\nContext Facts = {len(context.results)}:")
        for i, fact in enumerate(context.results, 1):
            print(f"  {i}. {fact.content}")

    async def search(self, query: str):
        results = await self.memory.query(query)
        print(f"\nFound {len(results.results)} memories:")
        for i, mem in enumerate(results.results, 1):
            sim = mem.metadata.get('similarity', 0) if mem.metadata else 0
            print(f"  {i}. {mem.content} [similarity={sim:.2f}]")

    async def clear(self):
        await self.memory.clear()
        existing_user_facts.clear()
        print("All memories cleared.")

    async def close(self):
        await self.memory.close()