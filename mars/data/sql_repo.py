import os
from rich.console import Console
from sqlalchemy import select
import faiss

# project imports
from mars.data.tables import EmbeddedDocument, Sentence


class SqlRepository:
    def __init__(self, session, faiss_repo):
        self.console = Console()
        self.session = session
        self.faiss_repo = faiss_repo


        self.index = self.get_faiss_index()

    def get_faiss_index(self):
        if not os.path.exists('index.faiss'):
            self.console.print('creating faiss index...')
            model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
            dimension = model.get_sentence_embedding_dimension()
            index = faiss.IndexFlatL2(dimension)
            faiss.write_index(index, 'index.faiss')
        index = faiss.read_index('index.faiss')
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
