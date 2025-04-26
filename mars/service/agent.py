from fastapi.logger import logger

# project imports
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm
        self.rag = None

    def run_query(self,
                  enable_rag: bool,
                  system_message: str,
                  query: str) -> str:
        logger.info(f'[Agent] Running query with {self.lm.name}')
        logger.info(f'[Agent] Running query with RAG: {enable_rag}')
        logger.debug(f'[Agent] Query: {query}')

        if enable_rag:
            docs = self.rag.retrieve_documents(query)
            logger.info(f'[Agent] Retrieved docs...')
            prompt = preprompt.format(docs=docs, query=query)
        else:
            prompt = preprompt.format(query=query)

        res = self.lm.generate(prompt)
        logger.info(f'[Agent] LLM response generated...')
        return res

    def set_rag(self, rag: RAG):
        self.rag = rag
