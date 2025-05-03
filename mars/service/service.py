from fastapi.logger import logger
from sentence_transformers import SentenceTransformer

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository
from mars.service.lm import LanguageModel
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


def run_query(base_url: str,
              lm_name: str,
              system_message: str,
              query: str,
              rag: RAG = None) -> str:
    lm = LanguageModel(name=lm_name, base_url=base_url)
    logger.info(f'[Baseline] Running query with {lm.name}')

    if rag:
        docs = rag.retrieve_documents(query)
        logger.info(f'[Baseline] Retrieved docs...')
        doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
        system_message = '\n'.join([system_message, doc_msg])

    res = lm.chat(system_message=system_message, query=query)
    logger.debug(f'[Baseline] LLM response generated: {res}')
    return res
