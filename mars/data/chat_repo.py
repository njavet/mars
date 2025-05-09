from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.conf.conf import CHAT_DB_URL


class ChatRepository:
    def __init__(self, db_path: Path = CHAT_DB_URL):
        self.db = TinyDB(db_path)