import subprocess

# project imports
from mars.data.chat_repo import ChatRepository
from mars.data.eval_repo import EvalRepository


def get_username() -> str:
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    return username


def get_chat_repo() -> ChatRepository:
    return ChatRepository()


def get_eval_repo() -> EvalRepository:
    return EvalRepository()

