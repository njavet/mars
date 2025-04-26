import numpy as np
from fastapi.logger import logger
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME, L2_THRESHOLD
from mars.schemas import RagDocument
from mars.data.sql_repo import SqlRepository


class RAG:
    def __init__(self, sql_repo: SqlRepository) -> None:
        self.model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
        self.sql_repo = sql_repo

    def retrieve_documents(self,
                           query: str,
                           k: int = 5,
                           threshold: float = L2_THRESHOLD) -> list[RagDocument]:
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        qa = np.array([query_embedding])
        distances, indices = self.sql_repo.faiss_repo.search_index(qa, k)
        documents = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                logger.info(f'[RAG] recv doc with distance {distances[0][i]}')
                if distances[0][i] < threshold:
                    sentence = self.sql_repo.get_sentence(idx)
                    rag_doc = RagDocument(text=sentence.text,
                                          source=sentence.source,
                                          page_number=sentence.page_number,
                                          distance=distances[0][i])
                    documents.append(rag_doc)
        return documents
