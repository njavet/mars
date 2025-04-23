from langchain_ollama import ChatOllama


class OllamaLM:
    def __init__(self, name: str, base_url: str):
        self.lm = ChatOllama(base_url=base_url, model=name)

    def generate(self,
                 prompt: str,
                 max_tokens: int = 512,
                 temperature: float = 1.) -> str:
        res = self.lm.invoke(prompt)
        return res.text()
