import requests
import subprocess

# project imports
from mars.schema.res import SystemMessage
from mars.db.chat_repo import ChatRepository
from mars.db.eval_repo import EvalRepository
from mars.engine.prompts import prompts, medical


def get_username() -> str:
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    return username


def get_chat_repo() -> ChatRepository:
    return ChatRepository()


def get_eval_repo() -> EvalRepository:
    return EvalRepository()


def get_models(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    models = [model['name'] for model in data.get('models', [])]
    return models


def load_system_messages():
    lst = []
    for name in dir(medical):
        if not name.startswith('_'):
            text = getattr(medical, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    for name in dir(prompts):
        if not name.startswith('_'):
            text = getattr(prompts, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    return lst
