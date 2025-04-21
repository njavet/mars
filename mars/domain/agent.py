from typing import Protocol


class Agent(Protocol):
    """
    For now we define an Agent as an entity that can run a query. Some agents may use an LLM,
    others something else.
    """
    name: str

    def run_query(self, query: str) -> str:
        ...
