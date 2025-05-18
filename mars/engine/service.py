from fastapi.logger import logger
import requests

# project imports
from mars.schema.llm import Message
from mars.schema.req import LLMSpec
from mars.db.chat_repo import ChatRepository
# TODO llm factory
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.llm.transformer_llm import TransformerLLM
from mars.engine.parsing import parse_text_to_llm_input


def get_models(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    models = [model['name'] for model in data.get('models', [])]
    return models


def run_chat(llm_spec: LLMSpec,
             messages: list[Message],
             username: str,
             repo: ChatRepository) -> str:

    chat = repo.get_chat(username)
    logger.info(f'Running query with {llm_spec.model_name}')
    if llm_spec.base_url:
        llm = OllamaLLM(base_url=llm_spec.base_url, model=llm_spec.model_name)
    else:
        llm = TransformerLLM(model_name=llm_spec.model_name)

    if llm_spec.chat_mode:
        system_message = parse_text_to_llm_input(payload.system_message)
        messages = [{'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': payload.user_message}]
        res = llm.chat(messages)
    else:
        # TODO implement generate
        res = {}
    logger.info(f'LLM response generated...')
