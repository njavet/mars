import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# project imports
from mars.schema.eval import ScoreEntry, EvalDoc
from mars.db.eval_repo import EvalRepository


@pytest.fixture
def in_memory_repo(monkeypatch):
    def tinydb_memory_patch(*args, **kwargs):
        return TinyDB(storage=MemoryStorage)
    monkeypatch.setattr('mars.db.eval_repo.TinyDB', tinydb_memory_patch)
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


@pytest.fixture
def fake_run():
    return EvalDoc(run=0,
                   server='hyperion',
                   filename='test.docx',
                   system_message='test',
                   chat_api=True,
                   system_message_role='user',
                   lms={
                       'skynet': 'I generated something',
                       'legion': 'I did not'})


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


def test_set_and_get_run(in_memory_repo, fake_run):
    latest_run = in_memory_repo.get_latest_run()
    assert latest_run == 0
    in_memory_repo.save_eval_doc(fake_run)
    latest_run = in_memory_repo.get_latest_run()
    assert latest_run == 1


def test_get_eval_doc(in_memory_repo, fake_run):
    in_memory_repo.save_eval_doc(fake_run)
    eval_docs = in_memory_repo.get_eval_docs(run=0)
    assert len(eval_docs) == 1
    assert eval_docs[0].lms['skynet'] == 'I generated something'
    assert eval_docs[0].lms['legion'] == 'I did not'


