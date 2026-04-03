# Week 7 - RAG + Multimodal AI System

This week was developed as a single integrated AI system, built incrementally across five days.  
The day-wise folders show the progression of the work, while the main `src/` folder contains the final consolidated implementation.

---

## Folder Structure

```text
Week-7/
├── .venv/
├── Day-1/
│   ├── images/
│   ├── src/
│   │   ├── embeddings/
│   │   │   └── embedder.py
│   │   ├── pipelines/
│   │   │   └── ingest.py
│   │   ├── retriever/
│   │   │   └── query_engine.py
│   │   └── vectorstore/
│   │       └── index.faiss
│   └── RAG-ARCHITECTURE.md
├── Day-2/
│   ├── images/
│   ├── src/
│   │   ├── pipelines/
│   │   │   └── context_builder.py
│   │   └── retriever/
│   │       ├── hybrid_retriever.py
│   │       └── reranker.py
│   └── RETRIEVAL-STRATEGIES.md
├── Day-3/
│   ├── images/
│   ├── src/
│   │   ├── embeddings/
│   │   │   └── clip_embedder.py
│   │   ├── pipelines/
│   │   │   └── image_ingest.py
│   │   └── retriever/
│   │       └── image_search.py
│   └── MULTIMODAL-RAG.md
├── Day-4/
│   ├── images/
│   ├── src/
│   │   ├── generator/
│   │   │   └── sql_generator.py
│   │   ├── pipelines/
│   │   │   └── sql_pipeline.py
│   │   └── utils/
│   │       └── schema_loader.py
│   └── SQL-QA-DOC.md
├── Day-5/
│   ├── images/
│   ├── src/
│   │   ├── deployment/
│   │   │   └── app.py
│   │   ├── evaluation/
│   │   │   └── rag_eval.py
│   │   └── memory/
│   │       └── memory_store.py
│   ├── CHAT-LOGS.json
│   └── DEPLOYMENT-NOTES.md
├── src/
│   ├── __pycache__/
│   ├── config/
│   │   ├── __pycache__/
│   │   └── model.yaml
│   ├── data/
│   │   ├── chunks/
│   │   ├── images/
│   │   ├── raw/
│   │   ├── enterprise.db
│   │   └── products.csv
│   ├── deployment/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── app.py
│   ├── embeddings/
│   │   ├── __pycache__/
│   │   ├── clip_embedder.py
│   │   └── embedder.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── rag_eval.py
│   ├── generator/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   └── sql_generator.py
│   ├── logs/
│   ├── memory/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── memory_store.py
│   ├── pipelines/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── context_builder.py
│   │   ├── image_ingest.py
│   │   ├── ingest.py
│   │   └── sql_pipeline.py
│   ├── retriever/
│   ├── ui/
│   │   └── app.py
│   ├── utils/
│   │   ├── __pycache__/
│   │   └── schema_loader.py
│   ├── vectorstore/
│   │   ├── image_index.faiss
│   │   ├── image_metadata.db
│   │   ├── index.faiss
│   │   └── index.pkl
│   ├── __init__.py
│   ├── .env
│   ├── db_setup.py
│   ├── run_sql_qa.py
│   └── test_search.py
├── temp_uploaded/
├── temp_uploads/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Project Structure Explanation

### Day-wise folders

The `Day-1` to `Day-5` folders are kept to show the weekly progression clearly.

- Each day represents a specific deliverable.
- They document how the system evolved step by step.
- They are useful for learning, review, and presentation.

### Main `src/` folder

The main `src/` folder contains the final integrated implementation.

It combines everything developed during the week into one structured system, including:

- text embeddings
- image embeddings
- ingestion pipelines
- retrieval logic
- multimodal search
- SQL query generation
- evaluation
- deployment
- memory handling
- vector storage

### Why both structures are kept

This week was interrelated, so both views are important:

- `Day-*` folders show the development journey
- `src/` shows the final complete working system

This makes the project easier to understand and present.