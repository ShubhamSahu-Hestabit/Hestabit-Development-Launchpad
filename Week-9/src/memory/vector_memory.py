import faiss
import pickle
import os
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from autogen_core.memory import Memory, MemoryContent, MemoryMimeType, MemoryQueryResult, UpdateContextResult


class FAISSVectorMemory(Memory):
    """Vector memory — stores embeddings in FAISS for similarity-based recall."""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        k: int = 3,
        score_threshold: float = 0.3,
        persist_path: Optional[str] = "db/vector_store.faiss"
    ):
        self.k = k
        self.score_threshold = score_threshold
        self.persist_path = persist_path

        self.encoder = SentenceTransformer(embedding_model)
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.contents: List[MemoryContent] = []

        if persist_path and os.path.exists(persist_path):
            self._load()

    async def add(self, content: MemoryContent):
        embedding = self.encoder.encode([content.content], convert_to_numpy=True)
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.contents.append(content)
        if self.persist_path:
            self._save()

    async def query(self, query: str) -> MemoryQueryResult:
        if len(self.contents) == 0:
            return MemoryQueryResult(results=[])

        query_embedding = self.encoder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)

        k = min(self.k, len(self.contents))
        distances, indices = self.index.search(query_embedding, k)
        similarities = 1 - (distances[0] ** 2) / 2

        results = []
        for idx, score in zip(indices[0], similarities):
            if score >= self.score_threshold:
                content = self.contents[idx]
                if content.metadata is None:
                    content.metadata = {}
                content.metadata["similarity"] = float(score)
                results.append(content)

        return MemoryQueryResult(results=results)

    async def update_context(self, model_context) -> UpdateContextResult:
        # Vector memory is query-driven only — not auto-injected
        return UpdateContextResult(memories=MemoryQueryResult(results=[]))

    async def clear(self):
        self.index.reset()
        self.contents.clear()
        if self.persist_path and os.path.exists(self.persist_path):
            os.remove(self.persist_path)
            meta = f"{self.persist_path}.meta"
            if os.path.exists(meta):
                os.remove(meta)

    async def close(self):
        if self.persist_path:
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        faiss.write_index(self.index, self.persist_path)
        with open(f"{self.persist_path}.meta", 'wb') as f:
            pickle.dump(self.contents, f)

    def _load(self):
        self.index = faiss.read_index(self.persist_path)
        with open(f"{self.persist_path}.meta", 'rb') as f:
            self.contents = pickle.load(f)

    def __len__(self):
        return len(self.contents)