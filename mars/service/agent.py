# project imports
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG



class Agent:
    def __init__(self, lm: LanguageModel, rag: RAG):
        self.lm = lm
        self.rag = rag

    def run_query(self, query: str) -> str:
        return self.lm.generate(query)


def get_agent(lm_name, base_url):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    repo =
    agent = Agent(lm)
    return agent
