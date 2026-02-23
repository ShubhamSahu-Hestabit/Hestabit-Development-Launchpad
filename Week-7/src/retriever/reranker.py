from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=5):
        if not documents:
            return []

        pairs = [(query, doc["content"]) for doc in documents]
        scores = self.model.predict(pairs)

        for i in range(len(documents)):
            documents[i]["rerank_score"] = float(scores[i])

        documents = sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return documents[:top_k]