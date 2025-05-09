import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# project imports
from mars.schemas import ScoreEntry
from mars.data.eval_repo import EvalRepository


@pytest.fixture
def in_memory_repo(monkeypatch):
    def tinydb_memory_patch(*args, **kwargs):
        return TinyDB(storage=MemoryStorage)
    monkeypatch.setattr('mars.data.eval_repo.TinyDB', tinydb_memory_patch)
    return EvalRepository()


@pytest.fixture
def fake_scores():
    fs = [
        ScoreEntry(run=0,
                   filename='test.docx',
                   lm_name='skynet',
                   scores={'complete': 'yes',
                           'irrelevant': 'no',
                           'concise': 'yes'}),
        ScoreEntry(run=0,
                   filename='test.docx',
                   lm_name='HAL-9000',
                   scores={'complete': 'no',
                           'irrelevant': 'no',
                           'concise': 'yes'}),
        ScoreEntry(run=0,
                   filename='test.docx',
                   lm_name='nautilus:5b',
                   scores={'complete': 'yes',
                           'irrelevant': 'no',
                           'concise': 'no'}),
        ScoreEntry(run=0,
                   filename='second_test.docx',
                   lm_name='skynet',
                   scores={'complete': 'no',
                           'irrelevant': 'no',
                           'concise': 'yes'}),
    ]
    return fs


def test_set_and_get_scores(in_memory_repo, fake_scores):
    in_memory_repo.save_scores(fake_scores)
    scores = in_memory_repo.get_scores(run=0)
    assert len(scores) == len(fake_scores)
    assert scores[0].lm_name == 'skynet'
    assert scores[1].scores['complete'] == 'no'

    se = ScoreEntry(run=0,
                    filename='test.docx',
                    lm_name='nautilus:5b',
                    scores={'complete': 'no',
                            'irrelevant': 'yes',
                            'concise': 'no'})
    in_memory_repo.set_score(se)
    scores = in_memory_repo.get_scores(run=0)
    assert scores[2].scores['complete'] == 'no'
