
# project imports
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository
from mars.service.lm import LanguageModel
from mars.service.agent import Agent
from mars.service.rag import RAG
from mars.service.embedder import EmbeddingService


def create_embeddings():
    with session_factory.get_session() as session:
        sql_repo = SqlRepository(session, faiss_repo)
        es = EmbeddingService(model, sql_repo)
        es.embed_documents()


def get_agent(base_url, lm_name, session):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
    index_dimension = model.get_sentence_embedding_dimension()
    faiss_repo = FaissRepository(index_dimension)
    sql_repo = SqlRepository(session, faiss_repo)
    rag = RAG(sql_repo)
    agent.set_rag(rag)
    return agent
