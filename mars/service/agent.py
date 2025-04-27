from abc import ABC, abstractmethod

# project imports
from mars.service.lm import LanguageModel


class BaseAgent(ABC):
    def __init__(self, lm: LanguageModel):
        self.lm = lm

    @abstractmethod
    def run_query(self, system_message: str, query: str) -> str:
        ...
