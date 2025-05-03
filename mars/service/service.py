from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository
from mars.service.rag import RAG


def init_rag():
    session_factory = SessionFactory()
    st_model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
    faiss_repo = FaissRepository(
        dim=st_model.get_sentence_embedding_dimension())
    sql_repo = SqlRepository(session_factory=session_factory,
                             faiss_repo=faiss_repo)
    rag = RAG(st_model, sql_repo)
    return rag
