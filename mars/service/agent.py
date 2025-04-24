# project imports
from mars.utils.prompt import get_prompt
from mars.service.lm import LanguageModel


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm

    def run_query(self, query: str) -> str:
        prompt = get_prompt()
        full_prompt = prompt.format(doc_text=query)
        return self.lm.generate(full_prompt)


def get_agent(lm_name, base_url):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    return agent
