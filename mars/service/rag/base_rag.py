from abc import ABC
from sentence_transformers import SentenceTransformer
from pathlib import Path

# project imports
from mars.service.rag.base_embedder import BaseEmbedder


class BaseRAG(ABC):
    def __init__(self,
                 sentence_transformer_name: str,
                 doc_folder: Path) -> None:
        self.sentence_transformer_name = sentence_transformer_name
        self.model = self.create_sentence_transformer()
        self.embedder = BaseEmbedder(self.model,
                                     doc_folder)

    def create_sentence_transformer(self):
        return SentenceTransformer(self.sentence_transformer_name)

    def retrieve_documents(self, query: str, k: int):
        raise NotImplementedError
