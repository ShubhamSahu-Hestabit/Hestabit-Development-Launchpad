from autogen_core.memory import Memory, MemoryContent, MemoryMimeType, MemoryQueryResult, UpdateContextResult


class SessionMemory(Memory):
    """Short-term memory — stores last N conversation turns in-memory."""

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.turns = []

    async def add(self, content: MemoryContent):
        self.turns.append(content.content)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    async def query(self, query: str) -> MemoryQueryResult:
        return MemoryQueryResult(results=[
            MemoryContent(content=text, mime_type=MemoryMimeType.TEXT)
            for text in self.turns
        ])

    async def update_context(self, model_context) -> UpdateContextResult:
        return UpdateContextResult(memories=await self.query(""))

    async def clear(self):
        self.turns = []

    async def close(self):
        pass

    def __len__(self):
        return len(self.turns)