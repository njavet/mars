from abc import ABC
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.repo import Repository


class BaseRAG(ABC):
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
        self.model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
        self.embedder = None

    def retrieve_documents(self, query: str, k: int):
        raise NotImplementedError
