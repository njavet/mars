from sys import pycache_prefix
from typing import Any
import json
import pprint
from fastapi.logger import logger
import requests

# project imports
from mars.schema.eval import Message


class OllamaLLM:
    def __init__(self,
                 model_name: str,
                 base_url: str = 'http://localhost:11434') -> None:
        self.model_name = model_name
        self.base_url = base_url

    def chat(self,
             messages: list[Message],
             options: dict[str, Any] = None) -> str:
        payload = {
            'model': self.model_name,
            'messages': [msg.model_dump() for msg in messages],
            'stream': False,
            'format': 'json',
        }
        if options:
            payload.update(options)
        res = requests.post(url=f'{self.base_url}/api/chat', json=payload)
        logger.info(f'[LLM] generated response on server: {self.base_url}')
        res.raise_for_status()
        res = res.json()
        self.log_llm_response(res)
        return res['message']['content']

    def chat_with_tools(self,
                        messages: list[Message],
                        tools: list,
                        options: dict[str, Any] = None) -> bool:
        payload = {
            'model': self.model_name,
            'messages': [msg.model_dump() for msg in messages],
            'stream': False,
            'format': 'json',
            'tools': tools,
        }
        if options:
            payload.update(options)
        res = requests.post(url=f'{self.base_url}/api/chat', json=payload)
        logger.info(f'[LLM] generated response on server: {self.base_url}')
        res.raise_for_status()
        res = res.json()
        tool_calls = res['message'].get('tool_calls', [])
        pprint.pprint(res)
        print('tool_calls', tool_calls)

        if isinstance(res, dict) and tool_calls:
            for tool in tool_calls:
                name = tool['function']['name']
                args = tool['function']['arguments']
                if name == 'analyze_diagnosis':
                    return True
                    # Inject tool output
        else:
            return False

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
            logger.info(f'[LM] generation time: {int(seconds)} s')
        except Exception as e:
            logger.warning(f'[LM] timing log failed: {e}')
