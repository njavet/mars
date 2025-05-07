import requests
from fastapi.logger import logger

# project imports
from mars.service.lm import LanguageModel
from mars.service.agent import Agent
from mars.service.rag import RAG


def get_lms(base_url: str):
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


def run_baseline(base_url: str,
                 lm_name: str,
                 system_message: str,
                 query: str,
                 chat_mode: bool = True) -> str:
    lm = LanguageModel(name=lm_name, base_url=base_url)
    logger.info(f'[Baseline] Running query with {lm.name}')
    if chat_mode:
        try:
            res = lm.chat_ollama(system_message=system_message, query=query)
        except:
            res = 'failed'
    else:
        res = lm.generate('\n'.join([system_message, query]))
    logger.info(f'[Baseline] LLM response generated...')
    return res


def run_baseline_rag(base_url: str,
                     lm_name: str,
                     system_message: str,
                     query: str,
                     rag: RAG,
                     chat_mode: bool = True) -> str:
    lm = LanguageModel(name=lm_name, base_url=base_url)
    logger.info(f'[Baseline RAG] Running query with {lm.name}')

    docs = rag.retrieve_documents(query)
    logger.info(f'[Baseline RAG] Retrieved docs...')
    doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
    system_message = '\n'.join([system_message, doc_msg])

    if chat_mode:
        res = lm.chat(system_message=system_message, query=query)
    else:
        res = lm.generate('\n'.join([system_message, query]))
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
