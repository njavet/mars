

class OllamaLM:
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url

    def generate(self,
                 prompt: str,
                 max_tokens: int,
                 temperature: float) -> str:
        pass
