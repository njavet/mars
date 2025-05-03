from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository


# singleton global instances
session_factory = SessionFactory()
st_model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
faiss_repo = FaissRepository(dim=st_model.get_sentence_embedding_dimension())


def get_session():
    return session_factory.get_session()


def get_st_model():
    return st_model


def get_faiss_repo():
    return faiss_repo

