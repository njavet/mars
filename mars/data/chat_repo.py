from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.conf.conf import CHAT_DB_URL
from mars.schemas import Message


class ChatRepository:
    def __init__(self, db_path: Path = CHAT_DB_URL):
        self.db = TinyDB(db_path)
        self.chats = self.db.table('chats')

    def get_chat(self, username):
        res = self.chats.search(Query().username == username)
        return res

    def save_chat(self, messages: list[Message], username: str):
        chat_messages = self.get_chat(username)
        if not messages:
            self.chats.insert({'username': username,
                               'messages': [msg.model_dump() for msg in messages]})



