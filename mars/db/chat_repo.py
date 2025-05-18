from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.conf import CHAT_DB_URL
from mars.schema.llm import Message


class ChatRepository:
    def __init__(self, db_path: Path = CHAT_DB_URL):
        self.db = TinyDB(db_path)
        self.chats = self.db.table('chats')

    def get_messages(self, username) -> list[Message]:
        q = Query()
        found = self.chats.get(q.username == username)
        msgs = found.get('messages') if found else []
        return msgs

    def save_chat(self, messages: list[Message], username: str) -> None:
        msgs = self.get_messages(username)
        if msgs:
            msgs.extend([msg.model_dump() for msg in messages])
            self.chats.update({'username': username, 'messages': msgs})
        else:
            self.chats.insert({'username': username, 'messages': messages})

    def append_turn(self,
                    system_message: str,
                    user_message: str,
                    assistant_message: str,
                    username: str) -> None:
        msgs = self.get_messages(username)
        # overwrite system message
        msgs[0].content = system_message
        msgs.extend([Message(role='user', content=user_message),
                     Message(role='assistant', content=assistant_message)])
        self.chats.update({'username': username, 'messages': msgs})
