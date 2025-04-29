from contextlib import contextmanager
from sentence_transformers import SentenceTransformer
from fastapi.logger import logger

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository
from mars.service.lm import LanguageModel
from mars.service.agents.base_agent import BaseAgent
from mars.service.agents.rag_agent import BaseRagAgent, RagAgent
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
                     agent_type,
                     system_message,
                     query):
        lm = LanguageModel(name=lm_name, base_url=base_url)
        if agent_type == 'base':
            agent = BaseAgent(lm)
            return agent.run_query(system_message, query)
        elif agent_type == 'rag':
            with self.get_repo() as repo:
                rag = RAG(self.st_model, repo)
                agent = BaseRagAgent(lm, rag)
                return agent.run_query(system_message, query)
        elif agent_type == 'agentic_rag':
            judge_lm = LanguageModel(name=lm_name, base_url=base_url, temperature=0.1)
            with self.get_repo() as repo:
                rag = RAG(self.st_model, repo)
                agent = RagAgent(lm, rag, judge_lm)
                return agent.run_query(system_message, query)
