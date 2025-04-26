from fastapi.logger import logger
import requests


class LanguageModel:
    def __init__(self,
                 name: str,
                 base_url: str,
                 temperature: float = 0) -> None:
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

    def get_system_message(self):
        pass

    def get_option(self):
        options = {'temperature': self.temperature,
                   'top_k': -1,
                   'top_p': 1.0}
        return options

    def generate(self, query: str) -> str:
        logger.info(f'[LM] generate response on server: {self.base_url} with temperature: {self.temperature}')
        res = requests.post(
            url=f'{self.base_url}/api/generate',
            json={'model': self.name,
                  'prompt': query,
                  'stream': False,
                  'options': self.get_option()}
        )
        res.raise_for_status()
        return res.json()['response']
