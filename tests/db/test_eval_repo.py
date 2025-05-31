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
                   model_name='skynet',
                   scores={'true_positives': 2,
                           'irrelevant': 0,
                           'concise': 1}),
        ScoreEntry(run=0,
                   filename='test.docx',
                   model_name='HAL-9000',
                   scores={'false_negatives': 2,
                           'irrelevant': 1,
                           'concise': 0}),
        ScoreEntry(run=0,
                   filename='test.docx',
                   model_name='nautilus:5b',
                   scores={'false_negatives': 0,
                           'irrelevant': 1,
                           'concise': 0}),
        ScoreEntry(run=0,
                   filename='second_test.docx',
                   model_name='skynet',
                   scores={'true_positives': 1,
                           'irrelevant': 2,
                           'concise': 3}),
    ]
    return fs


@pytest.fixture
def fake_run():
    return EvalDoc(run=0,
                   server='hyperion',
                   filename='test.docx',
                   system_message='test',
                   models={
                       'skynet': 'I generated something',
                       'legion': 'I did not'})


def test_set_and_get_scores(in_memory_repo, fake_scores):
    in_memory_repo.save_scores(fake_scores)
    scores = in_memory_repo.get_scores(run=0)
    assert len(scores) == len(fake_scores)
    assert scores[0].model_name == 'skynet'
    assert scores[1].scores['false_negatives'] == 2

    se = ScoreEntry(run=0,
                    filename='test.docx',
                    model_name='nautilus:5b',
                    scores={'false_negatives': 0,
                            'irrelevant': 1,
                            'concise': 0})
    in_memory_repo.set_score(se)
    scores = in_memory_repo.get_scores(run=0)
    assert scores[2].scores['false_negatives'] == 0


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
    assert eval_docs[0].models['skynet'] == 'I generated something'
    assert eval_docs[0].models['legion'] == 'I did not'


