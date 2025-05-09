from fastapi.logger import logger

# project imports
from mars.data.chat_repo import ChatRepository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class ChatService:
    def __init__(self, base_url: str, lm_name: str):
        self.base_url = base_url
        self.lm = LanguageModel(name=lm_name, base_url=base_url)
        self.repo = ChatRepository()

    def run_baseline(self,
                     system_message: str,
                     query: str,
                     chat_api: bool = True,
                     system_message_role: str = 'user') -> dict:
        logger.info(f'[Baseline] Running query with {self.lm.name}')
        if chat_api:
            res = self.lm.chat(system_message=system_message,
                               query=query,
                               system_message_role=system_message_role)
        else:
            # TODO implement generate
            res = {}
        logger.info(f'[Baseline] LLM response generated...')
        return res

    def run_baseline_rag(self,
                         system_message: str,
                         query: str,
                         rag: RAG,
                         chat_api: bool = True,
                         system_message_role: str = 'user') -> dict:
        logger.info(f'[Baseline RAG] Running query with {self.lm.name}')
        docs = rag.retrieve_documents(query)
        logger.info(f'[Baseline RAG] Retrieved docs...')
        doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
        system_message = '\n'.join([system_message, doc_msg])
        res = self.run_baseline(system_message=system_message,
                                query=query,
                                chat_api=chat_api,
                                system_message_role=system_message_role)
        logger.info(f'[Baseline RAG] LLM response generated...')
        return res
