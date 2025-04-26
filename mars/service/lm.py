from fastapi.logger import logger
import requests


class LanguageModel:
    def __init__(self, name: str, base_url: str) -> None:
        self.name = name
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
        logger.info(f'[LM] generate: {self.base_url}')
        res = requests.post(
            url=f'{self.base_url}/api/generate',
            json={'model': self.name, 'prompt': prompt, 'stream': False}
        )
        res.raise_for_status()
        return res.json()['response']
