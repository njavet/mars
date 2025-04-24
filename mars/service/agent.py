# project imports
from mars.service.lm import LanguageModel


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm

    def run_query(self, query: str) -> str:
        return self.lm.generate(query)
