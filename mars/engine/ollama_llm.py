from fastapi.logger import logger
import requests


class OllamaLLM:
    def __init__(self,
                 base_url: str,
                 name: str,
                 model: str,
                 context_window: int | None = None,
                 params: dict | None = None,
                 template: str | None = None) -> None:
        self.base_url = base_url
        self.name = name
        self.model = model
        self.context_window = context_window
        self.params = params
        self.template = template

    def generate(self, prompt: str) -> dict:
        payload = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            **self.params
        }
        res = requests.post(url=f'{self.base_url}/api/generate', json=payload)
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()

    def chat(self, messages: list[dict[str, str]]) -> dict:
        payload = {
            'model': self.name,
            'messages': messages,
            'stream': False,
            **self.params
        }
        res = requests.post(url=f'{self.base_url}/api/chat', json=payload)
        logger.info(f'[LM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()

"""
        try:
            tokens = res['prompt_eval_count']
            if tokens > 4000:
                logger.warn(f'[LM] prompt tokens: {tokens}')
            else:
                logger.info(f'[LM] prompt tokens: {tokens}')
        except KeyError:
            print('no prompt eval count', res)
        logger.info(f'[LM] prompt chars: {len(system_message + query)}')
        logger.info(f'[LM] output tokens: {res['eval_count']}')
        seconds = res['eval_duration'] / 1000000
        logger.info(f'[LM] generation time: {seconds}s')
        return res

"""