class LanguageModel:
    def __init__(self, name: str, base_url: str) -> None:
        self.name = name
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
        pass
