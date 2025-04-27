from contextlib import contextmanager
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository
from mars.service.lm import LanguageModel
from mars.service.agents.base_agent import BaseAgent
from mars.service.agents.rag_agent import RagAgent
from mars.service.rag import RAG


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
            rag = RAG(self.st_model, repo)
            rag.embed_documents()

    def handle_query(self,
                     base_url,
                     lm_name,
                     enable_rag,
                     system_message,
                     query):
        lm = LanguageModel(name=lm_name, base_url=base_url)
        if enable_rag:
            with self.get_repo() as repo:
                rag = RAG(self.st_model, repo)
                agent = RagAgent(lm, rag)
                return agent.run_query(system_message, query)
        else:
            agent = BaseAgent(lm)
            return agent.run_query(system_message, query)
