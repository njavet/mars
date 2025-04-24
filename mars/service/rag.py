import numpy as np
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.schemas import RagDocument
from mars.data.repo import Repository


class RAG:
    def __init__(self, repo: Repository) -> None:
        self.model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
        self.repo = repo

    def retrieve_documents(self,
                           query: str,
                           k: int = 5,
                           threshold: float = 3.0) -> list[RagDocument]:
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        qa = np.array([query_embedding])
        distances, indices = self.repo.search_index(qa, k)
        documents = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                if distances[0][i] < threshold:
                    sentence = self.repo.get_sentence(idx)
                    rag_doc = RagDocument(text=sentence.text,
                                          source=sentence.source,
                                          page_number=sentence.page_number,
                                          distance=distances[0][i])
                    documents.append(rag_doc)
        return documents
