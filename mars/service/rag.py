import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List


class RAG:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def build_index(self, texts: List[str]):
        self.documents = texts
        embeddings = self.embedder.encode(texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.documents[i] for i in indices[0]]
