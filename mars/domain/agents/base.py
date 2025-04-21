
class BaseAgent:
    def __init__(self, llm_name: str) -> None:
        self.llm_name = llm_name

    def run_query(self, query: str) -> str:
        pass