from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.conf import CHAT_DB_URL
from mars.schema.llm import Message


class ChatRepository:
    def __init__(self, db_path: Path = CHAT_DB_URL):
        self.db = TinyDB(db_path)
        self.chats = self.db.table('chats')

    def get_chat(self, username):
        q = Query()
        found = self.chats.get(q.username == username)
        return found

    def get_messages(self, username):
        q = Query()
        found = self.chats.get(q.username == username)
        return found.get('messages') if found else []

    def save_chat(self, messages: list[Message], username: str):
        msgs = self.get_messages(username)
        if msgs:
            msgs.extend([msg.model_dump() for msg in messages])
            self.chats.update({'username': username, 'messages': msgs})
        else:
            self.chats.insert({'username': username, 'messages': messages})
