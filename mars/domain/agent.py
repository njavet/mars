from typing import Protocol


class Agent(Protocol):
    def run_query(self, query: str) -> str:
        ...
