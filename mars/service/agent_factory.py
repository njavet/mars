from mars.service.agent import AgentService
from mars.service.llama_agent import LlamaAgent

class AgentFactory:
    def __init__(self):
        self.registry = {
            'llama': LlamaAgent,
        }

    def get_agent(self, model_name: str) -> AgentService:
        agent_class = self.registry.get(model_name)
        if not agent_class:
            raise ValueError(f'Unsupported agent model: {model_name}')
        return agent_class()
