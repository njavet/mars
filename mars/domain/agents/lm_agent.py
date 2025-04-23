# project imports
from mars.domain.lm import LanguageModel


class LMAgent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm

    def run_query(self, query: str) -> str:
        return self.lm.generate(query)
