from fastapi.logger import logger

# project imports
from mars.service.lm import LanguageModel
from mars.service.agent import Agent
from mars.service.rag import RAG


def run_baseline(base_url: str,
                 lm_name: str,
                 system_message: str,
                 query: str) -> str:
    lm = LanguageModel(name=lm_name, base_url=base_url)
    logger.info(f'[Baseline] Running query with {lm.name}')
    res = lm.chat(system_message=system_message, query=query)
    logger.info(f'[Baseline] LLM response generated...')
    return res


def run_baseline_rag(base_url: str,
                     lm_name: str,
                     system_message: str,
                     query: str,
                     rag: RAG) -> str:
    lm = LanguageModel(name=lm_name, base_url=base_url)
    logger.info(f'[Baseline RAG] Running query with {lm.name}')

    docs = rag.retrieve_documents(query)
    logger.info(f'[Baseline RAG] Retrieved docs...')
    doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
    system_message = '\n'.join([system_message, doc_msg])

    res = lm.chat(system_message=system_message, query=query)
    logger.info(f'[Baseline RAG] LLM response generated...')
    return res


def run_agentic(base_url: str,
                lm_name: str,
                system_message: str,
                query: str) -> str:
    return


def run_agentic_rag(base_url: str,
                    lm_name: str,
                    system_message: str,
                    query: str,
                    rag: RAG) -> str:
    return
