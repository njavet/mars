from fastapi.logger import logger
import requests

# project imports
from mars.schema.llm import Message
from mars.schema.req import LLMRequest
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


def run_chat(llm_req: LLMRequest,
             username: str,
             repo: ChatRepository) -> str:

    logger.info(f'Running query with {llm_req.model_name}')
    # llm = TransformerLLM(model_name='teknium/OpenHermes-2.5-Mistral-7B')
    if llm_req.base_url:
        llm = OllamaLLM(base_url=llm_req.base_url, model=llm_req.model_name)
    else:
        llm = TransformerLLM(model_name=llm_req.model_name)

    if llm_req.chat_mode:
        history = repo.get_messages(username)
        system_message = parse_text_to_llm_input(llm_req.system_message)
        history[0].content = system_message
        history.append(Message(role='user', content=llm_req.user_message))
        res = llm.chat(history)
        repo.append_turn(system_message, llm_req.user_message, res, username)
    else:
        # TODO implement generate
        res = ''
    logger.info(f'LLM response generated...')
    return res
