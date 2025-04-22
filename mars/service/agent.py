# project imports
from mars.domain.lm import LanguageModel


class LMAgentService:
    def __init__(self, lm_name: str):
        self.lm_name = lm_name

    def handle_query(self, query: str) -> str:
        return self.agent.run_query(query)
