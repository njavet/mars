from typing import Protocol

# project imports
from mars.schema.llm import Message


class LLM(Protocol):
    def chat(self, messages: list[Message]) -> str:
        ...
