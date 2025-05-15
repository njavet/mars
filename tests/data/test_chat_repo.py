import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# project imports
from mars.schemas import Message
from mars.data.chat_repo import ChatRepository


@pytest.fixture
def in_memory_repo(monkeypatch):
    def tinydb_memory_patch(*args, **kwargs):
        return TinyDB(storage=MemoryStorage)
    monkeypatch.setattr('mars.data.chat_repo.TinyDB', tinydb_memory_patch)
    return ChatRepository()


@pytest.fixture
def fake_messages():
    messages = [
        Message(role='system',
                content='I am a system message',
                lm_name='openhermes'),
        Message(role='user',
                content='some user message'),
        Message(role='assistant',
                content='some reply from openhermes',
                lm_name = 'openhermes'),
        Message(role='user',
                content='some other user message'),
    ]
    return messages


def test_set_and_get_chat(in_memory_repo, fake_messages):
    res = in_memory_repo.get_chat('epikur')
    in_memory_repo.save_chat(fake_messages, 'epikur')
    pass



