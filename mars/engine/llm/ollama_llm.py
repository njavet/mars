from fastapi.logger import logger
import requests

# project imports
from mars.schema.eval import Message


class OllamaLLM:
    def __init__(self, base_url: str, model_name: str) -> None:
        self.base_url = base_url
        self.model_name = model_name

    def chat(self, messages: list[Message]) -> str:
        payload = {
            'model': self.model_name,
            'messages': [msg.model_dump() for msg in messages],
            'stream': False,
        }
        res = requests.post(url=f'{self.base_url}/api/chat', json=payload)
        logger.info(f'[LLM] generated response on server: {self.base_url}')
        res.raise_for_status()
        res = res.json()
        self.log_llm_response(res)
        return res['message']['content']

    @staticmethod
    def log_llm_response(res: dict) -> None:
        try:
            tokens = res.get('prompt_eval_count')
            if tokens is not None:
                logger.info(f'[LM] prompt tokens: {tokens}')
            else:
                logger.warning('[LM] prompt_eval_count missing')
        except Exception as e:
            logger.warning(f'[LM] failed to log token count: {e} — {res}')

        try:
            logger.info(f'[LM] output tokens: {res.get("eval_count")}')
            seconds = res.get('eval_duration', 0) / 1_000_000_000
            logger.info(f'[LM] generation time: {int(seconds)}s')
        except Exception as e:
            logger.warning(f'[LM] timing log failed: {e}')
