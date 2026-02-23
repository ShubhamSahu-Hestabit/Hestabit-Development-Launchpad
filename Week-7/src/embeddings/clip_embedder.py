import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np


class CLIPEmbedder:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def embed_image(self, image_path):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_image_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.cpu().numpy()[0].astype("float32")

    def embed_text(self, text):
        # CLIP max token limit = 77
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_text_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features.cpu().numpy()[0].astype("float32")