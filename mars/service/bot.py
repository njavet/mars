from contextlib import contextmanager
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository


class Bot:
    def __init__(self):
        self.sf = SessionFactory()
        self.st_model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
        self.faiss_repo = FaissRepository(
            dim=self.st_model.get_sentence_embedding_dimension()
        )

    @contextmanager
    def get_repo(self):
        with self.sf.get_session() as session:
            repo = SqlRepository(session, self.faiss_repo)
            yield repo

    def create_embeddings(self):
        with self.get_repo() as repo:

    def yo(self):
        print('he')