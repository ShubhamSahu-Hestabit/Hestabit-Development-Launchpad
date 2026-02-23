import sqlite3
import numpy as np
from rank_bm25 import BM25Okapi
from collections import defaultdict

from src.retriever.query_engine import QueryEngine


class HybridRetriever:
    def __init__(self, db_path="src/data/chunks/chunks.db"):
        self.db_path = db_path
        self.dense = QueryEngine()

        self.documents = []
        self.metadata = []
        self.chunk_ids = []

        self._load_chunks()
        self._build_bm25()

    # -------------------------
    # Load chunks from SQLite
    # -------------------------
    def _load_chunks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT chunk_id, text, source, page, chunk_index, year, type
            FROM chunks
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            chunk_id, text, source, page, chunk_index, year, doc_type = row

            self.chunk_ids.append(chunk_id)
            self.documents.append(text)
            self.metadata.append({
                "chunk_id": chunk_id,
                "source": source,
                "page": page,
                "chunk_index": chunk_index,
                "year": year,
                "type": doc_type
            })

    # -------------------------
    # Build BM25
    # -------------------------
    def _build_bm25(self):
        tokenized = [doc.split() for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized)

    # -------------------------
    # Normalize scores
    # -------------------------
    def _normalize(self, scores):
        if scores is None:
            return scores
        scores = list(scores)
        if len(scores) == 0:
            return scores

        min_s = min(scores)
        max_s = max(scores)

        if max_s == min_s:
            return scores

        return [(s - min_s) / (max_s - min_s) for s in scores]

    # -------------------------
    # Apply metadata filters
    # -------------------------
    def _apply_filters(self, results, filters):
        if not filters:
            return results

        filtered = []
        for r in results:
            meta = r["metadata"]
            if all(meta.get(k) == v for k, v in filters.items()):
                filtered.append(r)

        return filtered

    # -------------------------
    # Deduplicate
    # -------------------------
    def _deduplicate(self, results):
        seen = set()
        unique = []

        for r in results:
            key = r["content"][:300]
            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique

    # -------------------------
    # Max Marginal Relevance
    # -------------------------
    def _mmr(self, results, top_k=5, lambda_param=0.7):
        if not results:
            return results

        selected = []
        candidates = results.copy()

        while candidates and len(selected) < top_k:
            if not selected:
                selected.append(candidates.pop(0))
                continue

            mmr_scores = []
            for cand in candidates:
                relevance = cand["score"]
                diversity = max(
                    [abs(cand["score"] - sel["score"]) for sel in selected],
                    default=0
                )
                mmr = lambda_param * relevance - (1 - lambda_param) * diversity
                mmr_scores.append(mmr)

            best_idx = int(np.argmax(mmr_scores))
            selected.append(candidates.pop(best_idx))

        return selected

    # -------------------------
    # Main Hybrid Search
    # -------------------------
    def search(self, query, top_k=5, filters=None, alpha=0.6):

        # ---- Dense Retrieval
        dense_results = self.dense.search(query, top_k=top_k * 3)
        dense_scores = self._normalize([r["score"] for r in dense_results])

        dense_dict = {}
        for i, r in enumerate(dense_results):
            cid = r["metadata"]["chunk_id"]
            dense_dict[cid] = {
                "content": r["content"],
                "metadata": r["metadata"],
                "score": alpha * dense_scores[i]
            }

        # ---- Sparse Retrieval
        sparse_raw = self.bm25.get_scores(query.split())
        sparse_scores = self._normalize(sparse_raw)

        sparse_dict = {}
        for i, score in enumerate(sparse_scores):
            cid = self.chunk_ids[i]
            sparse_dict[cid] = {
                "content": self.documents[i],
                "metadata": self.metadata[i],
                "score": (1 - alpha) * score
            }

        # ---- Fusion
        combined = defaultdict(lambda: {"content": "", "metadata": {}, "score": 0})

        for cid in set(dense_dict) | set(sparse_dict):
            if cid in dense_dict:
                combined[cid] = dense_dict[cid]

            if cid in sparse_dict:
                if not combined[cid]["content"]:
                    combined[cid] = sparse_dict[cid]
                else:
                    combined[cid]["score"] += sparse_dict[cid]["score"]

        results = list(combined.values())
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        # ---- Filters
        results = self._apply_filters(results, filters)

        # ---- Deduplication
        results = self._deduplicate(results)

        # ---- Keyword Fallback
        if not results:
            print("Keyword fallback activated.")
            results = sorted(
                sparse_dict.values(),
                key=lambda x: x["score"],
                reverse=True
            )

        # ---- MMR Diversification
        results = self._mmr(results, top_k=top_k)

        return results


if __name__ == "__main__":
    retriever = HybridRetriever()

    results = retriever.search(
        query="Explain the financial risks",
        top_k=5,
        filters={"type": "pdf"}
    )

    for r in results:
        print("\nScore:", r["score"])
        print("Metadata:", r["metadata"])
        print("Preview:", r["content"][:300])