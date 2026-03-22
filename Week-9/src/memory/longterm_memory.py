import sqlite3
from datetime import datetime
from autogen_core.memory import Memory, MemoryContent, MemoryMimeType, MemoryQueryResult, UpdateContextResult
from autogen_core.models import UserMessage


class LongTermMemory(Memory):
    """Long-term memory — persists facts and context in SQLite."""

    def __init__(self, db_path: str = "db/long_term.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance INTEGER DEFAULT 5,
                timestamp TEXT NOT NULL,
                UNIQUE(content, memory_type)
            )
        """)
        conn.commit()
        conn.close()

    async def add(self, content: MemoryContent, memory_type: str = "episodic", importance: int = 5):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR IGNORE INTO memories (content, memory_type, importance, timestamp) VALUES (?, ?, ?, ?)",
            (content.content, memory_type, importance, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    async def query(self, query: str = "", memory_type: str = None, limit: int = 20) -> MemoryQueryResult:
        conn = sqlite3.connect(self.db_path)
        if memory_type:
            cursor = conn.execute(
                "SELECT content FROM memories WHERE memory_type = ? ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (memory_type, limit)
            )
        else:
            cursor = conn.execute(
                "SELECT content FROM memories ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (limit,)
            )
        rows = cursor.fetchall()
        conn.close()
        return MemoryQueryResult(results=[
            MemoryContent(content=row[0], mime_type=MemoryMimeType.TEXT)
            for row in rows
        ])

    async def update_context(self, model_context) -> UpdateContextResult:
        query_result = await self.query(memory_type="semantic", limit=10)
        if query_result.results:
            for i, mem in enumerate(query_result.results, 1):
                await model_context.add_message(
                    UserMessage(content=f"User Info:\n{i}. {mem.content}", source="memory")
                )
        return UpdateContextResult(memories=query_result)

    async def clear(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM memories")
        conn.commit()
        conn.close()

    async def close(self):
        pass

    def get_all_semantic_facts(self):
        """Return all user facts for dedup tracking on startup."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT content FROM memories WHERE memory_type = 'semantic'")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]