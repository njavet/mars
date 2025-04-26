import os
from rich.console import Console
from sqlalchemy import select
import faiss
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import FAISS_INDEX
from mars.data.tables import EmbeddedDocument, Sentence


class FaissRepository:
    def __init__(self, dim: int):
        self.console = Console()
        self.index = self.get_faiss_index(dim)

    def get_faiss_index(self, dim):
        if not os.path.exists(FAISS_INDEX):
            self.console.print('creating faiss index...')
            index = faiss.IndexFlatL2(dim)
            faiss.write_index(index, FAISS_INDEX)
        index = faiss.read_index(FAISS_INDEX)
        return index

    def get_embedded_documents(self):
        stmt = select(EmbeddedDocument.name)
        return self.session.scalars(stmt).all()

    def add_embedding(self, embedding):
        self.index.add(embedding.reshape(1, -1))

    def save_faiss_index(self):
        faiss.write_index(self.index, 'index.faiss')

    def save_sentences(self, sentences: list[Sentence]):
        self.session.add_all(sentences)
        self.session.commit()

    def search_index(self, query_array, k):
        distances, indices = self.index.search(query_array, k)
        return distances, indices

    def get_sentence(self, faiss_index):
        stmt = (select(Sentence.text,
                       Sentence.source,
                       Sentence.page_number)
                .where(Sentence.faiss_index == int(faiss_index)))
        result = self.session.execute(stmt).one()
        return result
