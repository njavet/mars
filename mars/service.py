from fastapi.logger import logger
import requests

# project imports
from mars.schema.req import LLMSpec
from mars.data.chat_repo import ChatRepository
from mars.engine.ollama_llm import OllamaLLM
from mars.engine.parsing import parse_text_to_llm_input


def get_models(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    models = [model['name'] for model in data.get('models', [])]
    return models


def run_llm_request(payload: LLMSpec,
                    username: str,
                    repo: ChatRepository) -> str:

    chat = repo.get_chat(username)
    logger.info(f'Running query with {payload.model}')
    llm = OllamaLLM(base_url=payload.base_url, model=payload.model)

    if payload.chat_api:
        system_message = parse_text_to_llm_input(payload.system_message)
        messages = [{'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': payload.user_message}]
        res = llm.chat(messages)
    else:
        # TODO implement generate
        res = {}
    logger.info(f'LLM response generated...')
    print(res)
    try:
        tokens = res['prompt_eval_count']
        if tokens > 4000:
            logger.warn(f'[LM] prompt tokens: {tokens}')
        else:
            logger.info(f'[LM] prompt tokens: {tokens}')
    except KeyError:
        print('no prompt eval count', res)
    prompt_len = len(payload.system_message) + len(payload.user_message)
    logger.info(f'[LM] prompt chars: {prompt_len}')
    logger.info(f'[LM] output tokens: {res['eval_count']}')
    seconds = res['eval_duration'] / 1000000
    logger.info(f'[LM] generation time: {seconds}s')
    return res['message']['content']
