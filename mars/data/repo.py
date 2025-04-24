from sqlalchemy import select
import faiss

# project imports
from mars.data.tables import Sentence


class Repository:
    def __init__(self, session):
        self.session = session
        self.index = faiss.read_index('index.faiss')

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
