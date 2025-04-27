from fastapi.logger import logger

# project imports
from mars.service.agent import Agent
from mars.service.lm import LanguageModel



class BaseAgent(Agent):
    def __init__(self, lm: LanguageModel) -> None:
        super().__init__(lm)

    def run_query(self, system_message: str, query: str) -> str:
        logger.info(f'[Base Agent] Running query with {self.lm.name}')
        logger.debug(f'[Base Agent] Query: {query}')
        res = self.lm.chat(system_message=system_message, query=query)
        logger.debug(f'[Base Agent] LLM response generated: {res}')
        return res
