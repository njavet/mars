import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# project imports
from mars.schema.eval import Message
from mars.db.chat_repo import ChatRepository


@pytest.fixture
def in_memory_repo(monkeypatch):
    def tinydb_memory_patch(*args, **kwargs):
        return TinyDB(storage=MemoryStorage)
    monkeypatch.setattr('mars.db.chat_repo.TinyDB', tinydb_memory_patch)
    return ChatRepository()


@pytest.fixture
def fake_messages():
    messages = [
        Message(role='system',
                content='I am a system message'),
        Message(role='user',
                content='some user message'),
        Message(role='assistant',
                content='some reply from openhermes'),
        Message(role='user',
                content='some other user message'),
    ]
    return messages


def test_set_and_get_chat(in_memory_repo, fake_messages):
    msgs = in_memory_repo.get_messages('epikur')
    assert msgs == []
    in_memory_repo.save_chat(fake_messages, 'epikur')
    msgs = in_memory_repo.get_messages('epikur')
    assert len(msgs) == 4


def test_save_chat_system_message(in_memory_repo, fake_messages):
    in_memory_repo.save_chat(fake_messages, 'platon')
    in_memory_repo.append_turn(system_message='new system message',
                               user_message='new user message',
                               assistant_message='new assistant message',
                               username='platon')
    msgs = in_memory_repo.get_messages('platon')
    assert msgs[0].content == 'new system message'
    assert len(msgs) == 6
