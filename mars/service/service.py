from fastapi.logger import logger

# project imports
from mars.service.lm import LanguageModel
from mars.service.rag import RAG



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
