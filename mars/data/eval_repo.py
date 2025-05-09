from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.conf.conf import RESULT_DB_URL
from mars.schemas import EvalDoc, ScoreEntry


class EvalRepository:
    def __init__(self, db_path: Path = RESULT_DB_URL):
        self.db = TinyDB(db_path)
        self.runs = self.db.table('runs')
        self.scores = self.db.table('scores')

    def get_latest_run(self):
        return len(self.runs.all())

    def save_eval_doc(self, eval_doc: EvalDoc):
        self.runs.insert(eval_doc.model_dump())

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        res = self.runs.search(Query().run == run)
        return [EvalDoc(**doc) for doc in res]

    # TODO pydantic / align with UI
    def save_scores(self, scores: dict[str, dict[str, dict[str, str]]]):
        self.scores.insert(scores)

