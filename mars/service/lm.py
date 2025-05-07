from fastapi.logger import logger
import ollama
import requests


class LanguageModel:
    def __init__(self,
                 name: str,
                 base_url: str,
                 temperature: float = 0.6) -> None:
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

    def get_option(self):
        options = {'temperature': self.temperature,
                   'top_k': -1,
                   'top_p': 1.0}
        return options

    def generate(self, prompt: str) -> str:
        res = requests.post(
            url=f'{self.base_url}/api/generate',
            json={'model': self.name,
                  'stream': False,
                  'prompt': prompt}
        )
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()['response']

    def chat(self, system_message: str, query: str) -> str:
        logger.info(f'[LM] chat with system message: {system_message}')
        res = requests.post(
            url=f'{self.base_url}/api/chat',
            json={'model': self.name,
                  'stream': False,
                  'messages': [
                      {'role': 'system', 'content': system_message},
                      {'role': 'user', 'content': query}
                  ]}
        )
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()['message']['content']

    def chat_ollama(self, system_message: str, query: str) -> str:
        logger.info(f'[LM] ollama chat with system message: {system_message}')
        messages = [system_message, query]
        res = ollama.chat(model=self.name, messages=messages)
        return res['messages']['content']

