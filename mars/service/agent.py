# project imports
from mars.domain.lm import LanguageModel


class LMAgentService:
    def __init__(self, lm_name: str, base_url: str):
        self.lm_name = lm_name
        self.base_url = base_url

    def handle_query(self, query: str) -> str:
        return self.agent.run_query(query)
