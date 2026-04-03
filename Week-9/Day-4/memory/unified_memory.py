from autogen_core.memory import Memory, MemoryContent, MemoryQueryResult, UpdateContextResult
from session_memory import SessionMemory
from longterm_memory import LongTermMemory
from vector_memory import FAISSVectorMemory
class UnifiedMemory(Memory):
    """Combines session, long-term, and vector memory into one interface."""
    def __init__(
        self,
        session_max_turns: int = 10,
        vector_k: int = 3,
        vector_threshold: float = 0.3,
        db_path: str = "db/long_term.db",
        vector_path: str = "db/vector_store.faiss"
    ):
        self.session = SessionMemory(max_turns=session_max_turns)
        self.longterm = LongTermMemory(db_path=db_path)
        self.vector = FAISSVectorMemory(
            k=vector_k,
            score_threshold=vector_threshold,
            persist_path=vector_path
        )
    async def add(self, content: MemoryContent, memory_type: str = "episodic", importance: int = 5):
        await self.session.add(content)
        await self.longterm.add(content, memory_type=memory_type, importance=importance)
        await self.vector.add(content)
    async def query(self, query: str) -> MemoryQueryResult:
        return await self.vector.query(query)
    async def update_context(self, model_context) -> UpdateContextResult:
        return await self.longterm.update_context(model_context)
    async def clear(self):
        await self.session.clear()
        await self.longterm.clear()
        await self.vector.clear()
    async def close(self):
        await self.session.close()
        await self.longterm.close()
        await self.vector.close()