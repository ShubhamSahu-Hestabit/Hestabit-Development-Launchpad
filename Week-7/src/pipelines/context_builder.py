from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker


class ContextBuilder:
    def __init__(self, max_tokens=2000):
        self.retriever = HybridRetriever()
        self.reranker = Reranker()
        self.max_tokens = max_tokens

    def _optimize_context(self, docs):
        context = ""
        token_count = 0

        for doc in docs:
            tokens = len(doc["content"].split())
            if token_count + tokens > self.max_tokens:
                break

            context += doc["content"] + "\n\n"
            token_count += tokens

        return context.strip()

    def build_context(self, query, top_k=5, filters=None):

        hybrid_results = self.retriever.search(
            query=query,
            top_k=top_k * 2,
            filters=filters
        )

        reranked = self.reranker.rerank(
            query=query,
            documents=hybrid_results,
            top_k=top_k
        )

        context = self._optimize_context(reranked)

        trace = [
            {
                "chunk_id": r["metadata"]["chunk_id"],
                "source": r["metadata"]["source"],
                "page": r["metadata"]["page"],
                "chunk_index": r["metadata"]["chunk_index"],
                "year": r["metadata"]["year"],
                "type": r["metadata"]["type"]
            }
            for r in reranked
        ]

        return {
            "context": context,
            "trace": trace
        }


if __name__ == "__main__":
    builder = ContextBuilder()

    result = builder.build_context(
        query="Explain the financial risks",
        top_k=5,
        filters={"type": "pdf"}
    )

    print("\n========== FINAL CONTEXT ==========\n")
    print(result["context"][:1000])

    print("\n========== TRACEABILITY ==========\n")
    for t in result["trace"]:
        print(t)