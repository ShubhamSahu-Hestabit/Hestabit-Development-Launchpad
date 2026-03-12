# MULTIMODAL-RAG — Day 3: Image RAG Pipeline

A multimodal RAG pipeline supporting ingestion and retrieval of images, scanned PDFs, forms, and diagrams using CLIP embeddings, OCR, and BLIP captioning stored in a FAISS vector index backed by SQLite.

---

## Project Structure

```
src/
├── data/
│   └── images/              # Ingested images + PDF-converted pages
├── embeddings/
│   └── clip_embedder.py     # CLIP text & image embedding
├── pipelines/
│   └── image_ingest.py      # Ingestion: OCR + caption + embed + store
├── retriever/
│   └── image_search.py      # Query modes: text→image, image→image, image→text
└── vectorstore/
    ├── image_index.faiss    # FAISS vector index
    └── image_metadata.db    # SQLite: path, caption, ocr_text
```

---

## Stack

| Component | Technology |
|---|---|
| Embeddings | CLIP (ViT-B/32) — 512-dim vectors |
| Vector Index | FAISS Flat L2 |
| Metadata Store | SQLite |
| OCR | Tesseract |
| Captioning | BLIP |

---

## Ingestion Pipeline

`image_ingest.py` processes all images and PDFs in `src/data/images/`:

- Converts scanned PDFs page-by-page → `filename.pdf_page_N.png`
- Extracts OCR text via Tesseract
- Generates captions via BLIP
- Encodes CLIP embeddings and stores in FAISS
- Saves metadata (path, caption, ocr_text) to SQLite

```bash
python src/pipelines/image_ingest.py
```

---

## Query Modes

### 1. Text → Image

Find images semantically matching a text query.

```python
from src.retriever.image_search import search_by_text

results = search_by_text("pie chart percentage", top_k=3)
for r in results:
    print(r["path"], r["caption"])
```

**Test Images:**

| | | |
|---|---|---|
| ![piechart2](images/piechart2.png) | ![piechart2 pdf](images/piechart2.pdf_page_0.png) | ![piechart1](images/piechart1.png) |
| `piechart2.png` | `piechart2.pdf_page_0.png` | `piechart1.png` |

**Results:**
```
Path:    src/data/images/piechart2.png
Caption: a pie chart with the percentage of populations
OCR:     Population Pie Chart | Other 19.32% | China 18.47% | ...

Path:    src/data/images/piechart2.pdf_page_0.png
Caption: a pie chart with the percentage of people who are using the internet
OCR:     Population Pie Chart | Other 19.32% | Bangladesh 2.19% | ...

Path:    src/data/images/piechart1.png
Caption: a pie chart showing the percentage of the number of people in germany
OCR:     Germany | Greece | Iceland | Ireland | Italy | ...
```

---

### 2. Image → Image

Find visually similar images using CLIP image embeddings.

```python
from src.retriever.image_search import search_by_image

results = search_by_image("src/data/images/system_design3.jpeg", top_k=3)
for r in results:
    print(r["path"], r["caption"])
```

**Query Image:**

![system_design3](images/system_design3.jpeg)

**Results:**

| | | |
|---|---|---|
| ![system_design3](images/system_design3.jpeg) | ![network_diagram2](images/network_diagram2.png) | ![system_design4](images/system_design4.png) |
| `system_design3.jpeg` | `network_diagram2.png` | `system_design4.png` |

```
Path:    src/data/images/system_design3.jpeg
Caption: a diagram of the system

Path:    src/data/images/network_diagram2.png
Caption: a diagram of a network with a computer and a laptop

Path:    src/data/images/system_design4.png
Caption: a diagram showing the sales cycle
```

---

### 3. Image → Text Answer

Returns captions + OCR from similar images — ready to feed into an LLM as context.

```python
from src.retriever.image_search import image_to_text_answer

context = image_to_text_answer("src/data/images/system_design3.jpeg", top_k=3)
print(context)
```

**Results:**
```
Caption: a diagram of the system
OCR: Systems engineering focuses on ensuring the pieces work together to achieve the objectives of the whole

Caption: a diagram of a network with a computer and a laptop
OCR: Computer network architecture / Firewall / Laptop / Wireless AP / Network server

Caption: a diagram showing the sales cycle
OCR: Product and Category / Vendor and Product-vendor / Order and Order-line
```

---

### 4. PDF Support

Scanned PDFs are auto-converted to per-page PNGs during ingestion and indexed like any other image.

```python
results = search_by_image("src/data/images/piechart2.pdf_page_0.png", top_k=3)
```

**PDF Page Image:**

![piechart2 pdf](images/piechart2.pdf_page_0.png)

**Results:**
```
Path:    src/data/images/piechart2.pdf_page_0.png
Caption: a pie chart with the percentage of people who are using the internet

Path:    src/data/images/piechart2.png
Caption: a pie chart with the percentage of populations

Path:    src/data/images/piechart1.png
Caption: a pie chart showing the percentage of the number of people in germany
```

---

## How to Run

```bash
# Install dependencies
pip install faiss-cpu torch transformers pillow pytesseract pdf2image

# Ingest images
python src/pipelines/image_ingest.py

# Test all query modes
python src/test_search.py
```