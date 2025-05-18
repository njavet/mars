from functools import wraps
from fastapi.logger import logger
import requests

# project imports
from mars.schema.llm import Message


def log_llm_response(func):
    @wraps(func)
    def wrapper(self, messages: list[Message]) -> str:
        res = func(self, messages)
        try:
            tokens = res.get('prompt_eval_count')
            if tokens is not None:
                if tokens > 4000:
                    logger.warning(f'[LM] prompt tokens: {tokens}')
                else:
                    logger.info(f'[LM] prompt tokens: {tokens}')
            else:
                logger.warning('[LM] prompt_eval_count missing')
        except Exception as e:
            logger.warning(f'[LM] failed to log token count: {e} — {res}')

        try:
            logger.info(f'[LM] output tokens: {res.get("eval_count")}')
            seconds = res.get('eval_duration', 0) / 1_000_000
            logger.info(f'[LM] generation time: {seconds}s')
        except Exception as e:
            logger.warning(f'[LM] timing log failed: {e}')

        return res.get('message', {}).get('content')
    return wrapper


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

    # TODO return type / decorator
    @log_llm_response
    def chat(self, messages: list[Message]) -> dict[str, str]:
        payload = {
            'model': self.name,
            'messages': messages,
            'stream': False,
            **self.params
        }
        res = requests.post(url=f'{self.base_url}/api/chat', json=payload)
        logger.info(f'[LLM] generated response on server: {self.base_url}')
        res.raise_for_status()
        return res.json()
