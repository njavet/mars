from fastapi.logger import logger
import toml
import ollama
import requests


class LanguageModel:
    def __init__(self,
                 name: str,
                 base_url: str,
                 temperature: float = 0) -> None:
        self.name = name
        self.base_url = base_url
        self.temperature = temperature
        self.top_k = 0.95
        self.num_predict = 256
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
                  'top_p': self.top_p,
                  'num_predict': self.num_predict,
                  'stop': ['<|im_end|>', '<|im_start|>'],
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
                  'temperature': self.temperature,
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
        prompt = system_message.format(report=query)
        logger.debug(f'[LM] chat: {prompt}')
        messages = [{'role': 'user', 'content': prompt}]
        client = ollama.Client(host=self.base_url)
        res = client.chat(model=self.name,
                          messages=messages,
                          options={'temperature': 0, 'stream': False})
        logger.info(f'[LM] prompt tokens: {res['prompt_eval_count']}')
        logger.info(f'[LM] output tokens: {res['eval_count']}')
        logger.info(f'[LM] generation time: {res['eval_duration']}')

        return res['message']['content']
