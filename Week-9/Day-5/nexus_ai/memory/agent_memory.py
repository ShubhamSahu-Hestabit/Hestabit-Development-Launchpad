from typing import List, Any
from autogen_core.memory import Memory, MemoryContent, MemoryMimeType
from autogen_core.models import UserMessage
from memory.session_memory import SessionMemory
from memory.vector_memory import FAISSVectorMemory
from memory.long_term import LongTermMemory

class AgentMemorySystem(Memory):
    """Unified — session + vector + long-term."""
    def __init__(
        self,
        session_max_turns: int = 50,
        vector_k: int = 5,
        vector_threshold: float = 0.3,
        db_path: str = "vectorstore/agent_long_term.db",
        vector_persist_path: str = "vectorstore/agent_vectors.faiss"
    ):
        self.session   = SessionMemory(max_turns=session_max_turns)
        self.vector    = FAISSVectorMemory(k=vector_k, score_threshold=vector_threshold, persist_path=vector_persist_path)
        self.long_term = LongTermMemory(db_path=db_path)
    async def add(self, content: MemoryContent, store_long_term: bool = False) -> None:
        await self.session.add(content)
        await self.vector.add(content)
        if store_long_term:
            importance  = content.metadata.get("importance", 0) if content.metadata else 0
            memory_type = content.metadata.get("type", "episodic") if content.metadata else "episodic"
            await self.long_term.add(content, memory_type=memory_type, importance=importance)
    async def query(self, query: str) -> List[MemoryContent]:
        vector_results = await self.vector.query(query)
        lt_results     = await self.long_term.query(query, limit=5)
        seen, unique   = set(), []
        for m in vector_results + lt_results:
            if m.content not in seen:
                seen.add(m.content)
                unique.append(m)
        return unique
    async def save_important_fact(self, fact: str, importance: int = 8) -> None:
        content = MemoryContent(
            content=fact,
            mime_type=MemoryMimeType.TEXT,
            metadata={"importance": importance, "type": "semantic"}
        )
        await self.vector.add(content)
        await self.long_term.add(content, memory_type="semantic", importance=importance)
    async def clear_session(self) -> None:
        await self.session.clear()
    async def clear(self) -> None:
        await self.session.clear()
        await self.vector.clear()
        await self.long_term.clear()
    async def close(self) -> None:
        await self.session.close()
        await self.vector.close()
        await self.long_term.close()
    async def update_context(self, model_context: Any) -> None:
        session_memories = await self.session.query("")
        important = await self.long_term.get_important_memories(min_importance=7, limit=5)
        parts = []
        if session_memories:
            parts.append("Recent:\n" + "\n".join(f"{i+1}. {m.content}" for i, m in enumerate(session_memories[-5:])))
        if important:
            parts.append("Important:\n" + "\n".join(f"{i+1}. {m.content}" for i, m in enumerate(important)))
        if parts:
            await model_context.add_message(UserMessage(content="\n".join(parts), source="memory"))
    def get_memory_stats(self) -> dict:
        return {
            "session":   len(self.session),
            "vector":    len(self.vector),
            "long_term": self.long_term.get_stats()
        }