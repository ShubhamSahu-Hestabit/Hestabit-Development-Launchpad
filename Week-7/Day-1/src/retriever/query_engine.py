import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.vectorstores import FAISS
from embeddings.embedder import EmbeddingManager


class QueryEngine:
    def __init__(self, vectorstore_dir="src/vectorstore"):
        self.embedding_manager = EmbeddingManager()
        self.embedding_model = self.embedding_manager.get_model()

        self.vectorstore = FAISS.load_local(
            vectorstore_dir,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

    def search(self, query: str, top_k: int = 5):
        results = self.vectorstore.similarity_search_with_score(query, k=top_k)

        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })

        return formatted_results


if __name__ == "__main__":
    engine = QueryEngine()

    query = "Explain the main topic of this document"
    results = engine.search(query)

    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print("Score:", result["score"])
        print("Metadata:", result["metadata"])
        print("Preview:", result["content"][:400])
