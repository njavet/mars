import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

# project imports
from mars.schemas import ScoreEntry
from mars.data import eval_repo


@pytest.fixture
def in_memory_repo(monkeypatch):
    def tinydb_memory_patch(*args, **kwargs):
        return TinyDB(storage=MemoryStorage)
    monkeypatch.setattr('eval_repo.TinyDB', tinydb_memory_patch)
    return eval_repo.EvalRepository()

def test_set_and_get_scores():
    repo = EvalRepository()


