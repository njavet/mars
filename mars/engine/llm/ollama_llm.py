from fastapi.logger import logger
import requests

# project imports
from mars.schema.llm import Message


class OllamaLLM:
    def __init__(self,
                 base_url: str,
                 model: str,
                 name: str | None = None,
                 context_window: int | None = None,
                 params: dict | None = None,
                 template: str | None = None) -> None:
        self.base_url = base_url
        self.model = model
        self.name = model if name is None else name
        self.context_window = context_window
        self.params = {'temperature': 0} if params is None else params
        self.template = template

    def generate(self, prompt: str) -> dict:
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            **self.params
        }
        res = requests.post(url=f'{self.base_url}/api/generate', json=payload)
        logger.info(f'[LLM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()

    def chat(self, messages: list[Message]) -> str:
        payload = {
            'model': self.name,
            'messages': messages,
            'stream': False,
            **self.params
        }
        res = requests.post(url=f'{self.base_url}/api/chat', json=payload)
        logger.info(f'[LLM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()['message']['content']
