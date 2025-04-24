import numpy as np
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.utils.text_helpers import extract_pdfs
from mars.schemas import RagDocument
from mars.data.repo import Repository


class RAG:
    def __init__(self, repo: Repository) -> None:
        self.model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
        self.repo = repo

    def embed_documents(self):
        sentences = extract_pdfs()
        for idx, sentence in enumerate(sentences):
            embedding = self.model.encode(sentence.text)
            self.repo.add_embedding(embedding)
            sentence.faiss_index = idx
        self.repo.save_faiss_index()
        self.repo.save_sentences(sentences)

    def retrieve_documents(self,
                           query: str,
                           k: int = 5,
                           threshold: float = 2.0) -> list[RagDocument]:
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
