from abc import ABC
from sentence_transformers import SentenceTransformer
from pathlib import Path


class BaseEmbedder(ABC):
    """ abstract base embedder class """
    def __init__(self,
                 sentence_transformer: SentenceTransformer,
                 doc_folder: Path) -> None:
        self.model = sentence_transformer
        self.doc_folder = doc_folder

    def embed_documents(self):
        raise NotImplementedError
