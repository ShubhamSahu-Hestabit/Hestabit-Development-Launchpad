from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingManager:
    """
    Handles embedding model loading.
    """

    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.embedding_model = self._load_model()

    def _load_model(self):
        return HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def get_model(self):
        return self.embedding_model
