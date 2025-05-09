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

    def chat(self,
             system_message: str,
             query: str,
             system_message_role: str) -> dict:
        logger.info(f'[LM] chat with system message: {system_message}')
        res = requests.post(
            url=f'{self.base_url}/api/chat',
            json={'model': self.name,
                  'stream': False,
                  'temperature': self.temperature,
                  'messages': [
                      {'role': system_message_role, 'content': system_message},
                      {'role': 'user', 'content': query}
                  ]},
        ).json()
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        logger.info(f'[LM] prompt tokens: {res['prompt_eval_count']}')
        logger.info(f'[LM] output tokens: {res['eval_count']}')
        seconds = res['eval_duration'] / 1000000
        logger.info(f'[LM] generation time: {seconds}s')
        return res


def get_lms(base_url: str):
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms
