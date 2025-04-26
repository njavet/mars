from fastapi.logger import logger
import requests


class LanguageModel:
    def __init__(self,
                 name: str,
                 base_url: str,
                 temperature: float = 100) -> None:
        self.name = name
        self.base_url = base_url
        self.temperature = temperature

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: float) -> None:
        if temperature < 0:
            raise ValueError('temperature cannot be negative')
        self._temperature = temperature

    def generate(self, prompt: str) -> str:
        logger.info(f'[LM] generate: {self.base_url}')
        res = requests.post(
            url=f'{self.base_url}/api/generate',
            json={'model': self.name,
                  'prompt': prompt,
                  'temperature': self.temperature,
                  'stream': False}
        )
        res.raise_for_status()
        return res.json()['response']
