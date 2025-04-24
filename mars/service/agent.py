# project imports
from mars.service.lm import LanguageModel


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm

    def run_query(self, query: str) -> str:
        return self.lm.generate(query)


def get_agent(lm_name, base_url):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    return agent
