# project imports
from mars.data.chat_repo import ChatRepository


class ChatService:
    def __init__(self, repo: ChatRepository):
        self.repo = repo
