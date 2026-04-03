from typing import List, Optional, Any
import faiss
import pickle
import os
from autogen_core.memory import Memory, MemoryContent
from sentence_transformers import SentenceTransformer

class FAISSVectorMemory(Memory):
    """Vector memory — FAISS semantic search, persists to disk."""
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        k: int = 5,
        score_threshold: float = 0.3,
        persist_path: Optional[str] = "vectorstore/agent_vectors.faiss"
    ):
        self.encoder         = SentenceTransformer(embedding_model)
        self.k               = k
        self.score_threshold = score_threshold
        self.persist_path    = persist_path
        self.dimension       = self.encoder.get_sentence_embedding_dimension()
        self.index           = faiss.IndexFlatL2(self.dimension)
        self.contents: List[MemoryContent] = []

        if persist_path and os.path.exists(persist_path):
            self._load()

    async def add(self, content: MemoryContent) -> None:
        embedding = self.encoder.encode([content.content], convert_to_numpy=True)
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.contents.append(content)
        if self.persist_path:
            self._save()

    async def query(self, query: str) -> List[MemoryContent]:
        if not self.contents:
            return []
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
                content.metadata["similarity_score"] = float(score)
                results.append(content)
        return results

    async def clear(self) -> None:
        self.index.reset()
        self.contents.clear()
        if self.persist_path and os.path.exists(self.persist_path):
            os.remove(self.persist_path)
        meta = f"{self.persist_path}.meta"
        if os.path.exists(meta):
            os.remove(meta)

    async def close(self) -> None:
        if self.persist_path:
            self._save()

    async def update_context(self, model_context: Any) -> None:
        pass

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        faiss.write_index(self.index, self.persist_path)
        with open(f"{self.persist_path}.meta", 'wb') as f:
            pickle.dump(self.contents, f)

    def _load(self) -> None:
        self.index = faiss.read_index(self.persist_path)
        meta = f"{self.persist_path}.meta"
        if os.path.exists(meta):
            with open(meta, 'rb') as f:
                self.contents = pickle.load(f)

    def __len__(self) -> int:
        return len(self.contents)