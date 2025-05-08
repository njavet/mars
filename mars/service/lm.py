from fastapi.logger import logger
import toml
import ollama
import requests


class LanguageModel:
    def __init__(self,
                 name: str,
                 base_url: str,
                 temperature: float = 0.3) -> None:
        self.name = name
        self.base_url = base_url
        self.temperature = temperature
        self.top_k = -1
        self.top_p = 1.0

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: float) -> None:
        if temperature < 0:
            raise ValueError('temperature cannot be negative')
        self._temperature = temperature

    def build_prompt(self, system_message: str, query: str) -> str:
        sp = toml.load('mars/conf/prompts.toml')
        prompt = sp['openhermes-template']['system'].format(system=system_message,
                                                            query=query)
        return prompt

    def generate(self, prompt: str) -> str:
        res = requests.post(
            url=f'{self.base_url}/api/generate',
            json={'model': self.name,
                  'stream': False,
                  'temperature': self.temperature,
                  'prompt': prompt}
        )
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()

    def chat(self, system_message: str, query: str) -> str:
        logger.info(f'[LM] chat with system message: {system_message}')
        res = requests.post(
            url=f'{self.base_url}/api/chat',
            json={'model': self.name,
                  'stream': False,
                  'messages': [
                      {'role': 'system', 'content': system_message},
                      {'role': 'user', 'content': query}
                  ]},
        )
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()['message']['content']

    def chat_ollama(self, system_message: str, query: str) -> str:
        logger.info(f'[LM] ollama chat with system message: {system_message}')
        messages = [{'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': query}]
        res = ollama.chat(model=self.name, messages=messages)
        return res['message']['content']

