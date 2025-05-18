import subprocess

# project imports
from mars.db.chat_repo import ChatRepository
from mars.db.eval_repo import EvalRepository
from mars.utils.username import get_linux_username


def get_username() -> str:
    return get_linux_username()


def get_chat_repo() -> ChatRepository:
    return ChatRepository()


def get_eval_repo() -> EvalRepository:
    return EvalRepository()
