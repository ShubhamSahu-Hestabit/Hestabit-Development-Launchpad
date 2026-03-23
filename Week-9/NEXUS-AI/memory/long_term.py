import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from autogen_core.memory import Memory, MemoryContent, MemoryMimeType


class LongTermMemory(Memory):
    def __init__(self, db_path: str = "vectorstore/agent_long_term.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                mime_type TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                importance INTEGER DEFAULT 0
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance DESC)")
        conn.commit()
        conn.close()

    async def add(self, content: MemoryContent, memory_type: str = "episodic", importance: int = 0) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO memories (content, memory_type, mime_type, metadata, importance) VALUES (?, ?, ?, ?, ?)",
            (
                content.content,
                memory_type,
                content.mime_type.value if isinstance(content.mime_type, MemoryMimeType) else content.mime_type,
                json.dumps(content.metadata) if content.metadata else None,
                importance
            )
        )
        conn.commit()
        conn.close()

    async def query(self, query: str = "", memory_type: Optional[str] = None, limit: int = 10) -> List[MemoryContent]:
        conn = sqlite3.connect(self.db_path)
        if query:
            sql = "SELECT content, mime_type, metadata FROM memories WHERE content LIKE ?"
            params = [f"%{query}%"]
        else:
            sql = "SELECT content, mime_type, metadata FROM memories WHERE 1=1"
            params = []
        if memory_type:
            sql += " AND memory_type = ?"
            params.append(memory_type)
        sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [
            MemoryContent(content=r[0], mime_type=r[1], metadata=json.loads(r[2]) if r[2] else None)
            for r in rows
        ]

    async def get_important_memories(self, min_importance: int = 5, limit: int = 20) -> List[MemoryContent]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT content, mime_type, metadata FROM memories WHERE importance >= ? ORDER BY importance DESC, created_at DESC LIMIT ?",
            (min_importance, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            MemoryContent(content=r[0], mime_type=r[1], metadata=json.loads(r[2]) if r[2] else None)
            for r in rows
        ]

    async def clear(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM memories")
        conn.commit()
        conn.close()

    async def close(self) -> None:
        pass

    async def update_context(self, model_context: Any) -> None:
        pass

    def get_stats(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        episodic = conn.execute("SELECT COUNT(*) FROM memories WHERE memory_type='episodic'").fetchone()[0]
        semantic = conn.execute("SELECT COUNT(*) FROM memories WHERE memory_type='semantic'").fetchone()[0]
        avg = conn.execute("SELECT AVG(importance) FROM memories").fetchone()[0] or 0
        conn.close()
        return {"total": total, "episodic": episodic, "semantic": semantic, "avg_importance": round(avg, 2)}