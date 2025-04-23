# project imports
from mars.conf import LMS
from mars.domain.agents.lm_agent import LMAgent
from mars.domain.lms.ollama_lm import OllamaLM


class AgentFactory:
    def __init__(self):
        self.registry = {lm: OllamaLM for lm in LMS}

    def get_agent(self, model_name: str, base_url: str) -> LMAgent:
        lm_class = self.registry.get(model_name)
        if not lm_class:
            raise ValueError(f'Unsupported model: {model_name}')
        lm = lm_class(model_name, base_url)
        return LMAgent(lm)
