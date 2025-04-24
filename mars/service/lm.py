from typing import Protocol


class LanguageModel(Protocol):
    name: str
    base_url: str

    def generate(self,
                 prompt: str,
                 max_tokens: int,
                 temperature: float) -> str:
        ...
