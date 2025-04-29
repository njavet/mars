from fastapi.logger import logger

# project imports
from mars.service.agent import Agent
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class BaseRagAgent(Agent):
    def __init__(self, lm: LanguageModel, rag: RAG) -> None:
        super().__init__(lm)
        self.rag = rag

    def run_query(self, system_message: str, query: str) -> str:
        logger.info(f'[RAG Agent] Running query with {self.lm.name}')
        logger.debug(f'[RAG Agent] Query: {query}')

        docs = self.rag.retrieve_documents(query)
        logger.info(f'[RAG Agent] Retrieved docs...')
        doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
        system_message = '\n'.join([system_message, doc_msg])

        res = self.lm.chat(system_message=system_message, query=query)
        logger.debug(f'[RAG Agent] LLM response generated: {res}')
        return res


class RagAgent(BaseRagAgent):
    def __init__(self,
                 lm: LanguageModel,
                 rag: RAG,
                 judge_lm: LanguageModel,
                 max_iter: int = 3,
                 keep_top: int = 5,
                 target_score: int = 4) -> None:
        super().__init__(lm, rag)
        self.judge_lm = judge_lm
        self.max_iter = max_iter
        self.keep_top = keep_top
        self.target_score = target_score
