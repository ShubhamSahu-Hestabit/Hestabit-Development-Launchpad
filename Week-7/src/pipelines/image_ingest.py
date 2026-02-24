import os
import faiss
import sqlite3
import numpy as np
import pytesseract
import torch
from PIL import Image
from pdf2image import convert_from_path
from transformers import BlipProcessor, BlipForConditionalGeneration
from src.embeddings.clip_embedder import CLIPEmbedder


IMAGE_FOLDER = "src/data/images"
FAISS_PATH = "src/vectorstore/image_index.faiss"
DB_PATH = "src/vectorstore/image_metadata.db"

device = "cuda" if torch.cuda.is_available() else "cpu"

clip_embedder = CLIPEmbedder()

blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)


def init_db():
    os.makedirs("src/vectorstore", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            caption TEXT,
            ocr_text TEXT
        )
    """)

    conn.commit()
    conn.close()


def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")

    inputs = blip_processor(
        images=image,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        output = blip_model.generate(
            **inputs,
            max_new_tokens=30
        )

    return blip_processor.decode(output[0], skip_special_tokens=True)


def extract_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def process_single_image(path, embeddings, cursor):
    print(f"Processing: {path}")

    ocr_text = extract_ocr(path)
    caption = generate_caption(path)

    image_emb = clip_embedder.embed_image(path)
    caption_emb = clip_embedder.embed_text(caption)

    # truncate OCR manually for safety
    ocr_emb = clip_embedder.embed_text(ocr_text[:500] if ocr_text else " ")

    combined_embedding = (0.4 * image_emb + 0.3 * caption_emb + 0.3 * ocr_emb)
    embeddings.append(combined_embedding)

    cursor.execute("""
        INSERT INTO images (path, caption, ocr_text)
        VALUES (?, ?, ?)
    """, (path, caption, ocr_text))


def ingest():
    print("Starting Image Ingestion...")

    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    embeddings = []

    for file in os.listdir(IMAGE_FOLDER):
        path = os.path.join(IMAGE_FOLDER, file)

        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            process_single_image(path, embeddings, cursor)

        elif file.lower().endswith(".pdf"):
            print(f"Processing PDF: {file}")

            pages = convert_from_path(path)

            for i, page in enumerate(pages):
                temp_path = f"{path}_page_{i}.png"
                page.save(temp_path, "PNG")
                process_single_image(temp_path, embeddings, cursor)

    conn.commit()
    conn.close()

    if len(embeddings) == 0:
        print("No images found in folder.")
        return

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, FAISS_PATH)

    print("Multimodal ingestion complete.")
    print("Total images processed:", len(embeddings))


if __name__ == "__main__":
    ingest()