import faiss
import sqlite3
import numpy as np
from src.embeddings.clip_embedder import CLIPEmbedder


FAISS_PATH = "src/vectorstore/image_index.faiss"
DB_PATH = "src/vectorstore/image_metadata.db"

clip_embedder = CLIPEmbedder()
index = faiss.read_index(FAISS_PATH)


def get_metadata_by_ids(ids):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    results = []

    for idx in ids:
        cursor.execute(
            "SELECT path, caption, ocr_text FROM images WHERE id = ?",
            (idx + 1,)
        )
        row = cursor.fetchone()

        if row:
            results.append({
                "path": row[0],
                "caption": row[1],
                "ocr_text": row[2]
            })

    conn.close()
    return results


def search_by_text(query, top_k=3):
    query_emb = clip_embedder.embed_text(query)
    query_emb = np.array([query_emb]).astype("float32")

    distances, indices = index.search(query_emb, top_k)
    return get_metadata_by_ids(indices[0])


def search_by_image(image_path, top_k=3):
    query_emb = clip_embedder.embed_image(image_path)
    query_emb = np.array([query_emb]).astype("float32")

    distances, indices = index.search(query_emb, top_k)
    return get_metadata_by_ids(indices[0])


def image_to_text_answer(image_path, top_k=3):
    results = search_by_image(image_path, top_k)

    context = ""
    for r in results:
        context += f"\nCaption: {r['caption']}\nOCR: {r['ocr_text']}\n"

    return context