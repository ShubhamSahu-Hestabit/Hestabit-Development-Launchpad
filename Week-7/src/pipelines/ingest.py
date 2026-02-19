import os
import sys
import sqlite3
import hashlib
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from embeddings.embedder import EmbeddingManager


class IngestionPipeline:
    def __init__(self, data_dir="src/data/raw", vectorstore_dir="src/vectorstore"):
        self.data_dir = data_dir
        self.vectorstore_dir = vectorstore_dir
        self.documents = []
        self.chunked_docs = []
        self.embedding_manager = EmbeddingManager()

    # ---------------------------
    # File Loader Router
    # ---------------------------
    def _load_file(self, file_path):
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        elif file_path.endswith(".csv"):
            loader = CSVLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            print(f"Skipping unsupported file: {file_path}")
            return []
        return loader.load()

    # ---------------------------
    # Load Documents
    # ---------------------------
    def load_documents(self):
        print("Loading documents...")
        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)
            docs = self._load_file(file_path)
            self.documents.extend(docs)
        print(f"Loaded {len(self.documents)} pages.")

    # ---------------------------
    # Clean Text
    # ---------------------------
    def clean_documents(self):
        print("Cleaning documents...")
        for doc in self.documents:
            text = doc.page_content.strip()
            text = " ".join(text.split())
            doc.page_content = text

    # ---------------------------
    # Chunk Documents (Deterministic IDs)
    # ---------------------------
    def chunk_documents(self):
        print("Chunking documents...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(self.documents)

        for idx, chunk in enumerate(chunks):
            base_string = (
                chunk.page_content +
                str(chunk.metadata.get("source", "")) +
                str(chunk.metadata.get("page", ""))
            )

            chunk_hash = hashlib.md5(base_string.encode()).hexdigest()
            chunk.metadata["chunk_id"] = chunk_hash
            chunk.metadata["chunk_index"] = idx
            chunk.metadata["ingested_at"] = str(datetime.utcnow())

        self.chunked_docs = chunks
        print(f"Created {len(self.chunked_docs)} chunks.")

    # ---------------------------
    # Save Chunks to SQLite
    # ---------------------------
    def save_chunks_to_sqlite(self):
        print("Saving chunks to SQLite...")
        os.makedirs("src/data/chunks", exist_ok=True)

        conn = sqlite3.connect("src/data/chunks/chunks.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id TEXT PRIMARY KEY,
            text TEXT,
            source TEXT,
            page INTEGER,
            chunk_index INTEGER,
            ingested_at TEXT
        )
        """)

        for chunk in self.chunked_docs:
            cursor.execute("""
            INSERT OR REPLACE INTO chunks VALUES (?, ?, ?, ?, ?, ?)
            """, (
                chunk.metadata["chunk_id"],
                chunk.page_content,
                chunk.metadata.get("source", ""),
                chunk.metadata.get("page", 0),
                chunk.metadata.get("chunk_index", 0),
                chunk.metadata["ingested_at"]
            ))

        conn.commit()
        conn.close()

    # ---------------------------
    # Create FAISS Vector Store
    # ---------------------------
    def create_vectorstore(self):
        print("Creating FAISS index...")
        embeddings = self.embedding_manager.get_model()

        vectorstore = FAISS.from_documents(
            documents=self.chunked_docs,
            embedding=embeddings
        )

        vectorstore.save_local(self.vectorstore_dir)
        print("FAISS index saved.")

    # ---------------------------
    # Run Full Pipeline
    # ---------------------------
    def run(self):
        self.load_documents()
        self.clean_documents()
        self.chunk_documents()
        self.save_chunks_to_sqlite()
        self.create_vectorstore()


if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
