from mars.domain.agent import Agent


class AgentService:
    def __init__(self, agent: Agent):
        self.agent = agent

    def handle_query(self, query: str) -> str:
        return self.agent.run_query(query)
