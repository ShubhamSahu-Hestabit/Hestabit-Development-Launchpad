import sys
import os

# Fix path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from src.retriever.image_search import search_by_text, search_by_image, image_to_text_answer

BASE_DIR = ROOT_DIR
IMAGE_PATH = os.path.join(BASE_DIR, "src", "data", "images", "system_design3.jpeg")

# ── 1. Text → Image ──────────────────────────────────────────
print("=" * 40)
print("TEXT → IMAGE SEARCH")
print("=" * 40)
results = search_by_text("pie chart percentage", top_k=3)
if not results:
    print("No results found")
for r in results:
    print("\n---")
    print("Path:   ", r["path"])
    print("Caption:", r["caption"])
    print("OCR:    ", r["ocr_text"])

# ── 2. Image → Image ─────────────────────────────────────────
print("\n" + "=" * 40)
print("IMAGE → IMAGE SEARCH")
print("=" * 40)
print("Using image:", IMAGE_PATH)
results = search_by_image(IMAGE_PATH, top_k=3)
if not results:
    print("No results found")
for r in results:
    print("\n---")
    print("Path:   ", r["path"])
    print("Caption:", r["caption"])
    print("OCR:    ", r["ocr_text"])

# ── 3. Image → Text ──────────────────────────────────────────
print("\n" + "=" * 40)
print("IMAGE → TEXT ANSWER")
print("=" * 40)
context = image_to_text_answer(IMAGE_PATH, top_k=3)
if not context.strip():
    print("No context found")
else:
    print(context)
    
# ── 4. PDF Page → Image Search ───────────────────────────────
print("\n" + "=" * 40)
print("PDF PAGE → IMAGE SEARCH")
print("=" * 40)

PDF_IMAGE_PATH = os.path.join(BASE_DIR, "src", "data", "images", "piechart2.pdf_page_0.png")
print("Using PDF page image:", PDF_IMAGE_PATH)

results = search_by_image(PDF_IMAGE_PATH, top_k=3)
if not results:
    print("No results found")
for r in results:
    print("\n---")
    print("Path:   ", r["path"])
    print("Caption:", r["caption"])
    print("OCR:    ", r["ocr_text"])

# ── 5. Text query matching PDF content ───────────────────────
print("\n" + "=" * 40)
print("TEXT QUERY → PDF CONTENT")
print("=" * 40)

results = search_by_text("population pie chart", top_k=3)
if not results:
    print("No results found")
for r in results:
    print("\n---")
    print("Path:   ", r["path"])
    print("Caption:", r["caption"])
    print("OCR:    ", r["ocr_text"])