from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.core.conf import RESULT_DB_URL
from mars.schema.eval import EvalDoc, ScoreEntry


class EvalRepository:
    def __init__(self, db_path: Path = RESULT_DB_URL):
        self.db = TinyDB(db_path)
        self.runs = self.db.table('runs')
        self.scores = self.db.table('scores')

    def get_latest_run(self):
        all_runs = self.runs.all()
        if not all_runs:
            return 0
        return max(entry['run'] for entry in all_runs) + 1

    def save_eval_doc(self, eval_doc: EvalDoc):
        self.runs.insert(eval_doc.model_dump())

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        res = self.runs.search(Query().run == run)
        return [EvalDoc(**doc) for doc in res]

    def save_scores(self, scores: list[ScoreEntry]):
        for score in scores:
            self.set_score(score)

    def get_scores(self, run: int) -> list[ScoreEntry]:
        res = self.scores.search(Query().run == run)
        return [ScoreEntry(**doc) for doc in res]

    def set_score(self, score: ScoreEntry):
        q = Query()
        match = ((q.run == score.run) &
                 (q.filename == score.filename) &
                 (q.model_name == score.model_name))
        found = self.scores.get(match)
        if found:
            scores = found.get('scores', {})
            for key, value in score.scores.items():
                scores[key] = value
            self.scores.update({'scores': scores}, match)
        else:
            self.scores.insert({
                'run': score.run,
                'filename': score.filename,
                'model_name': score.model_name,
                'scores': score.scores}
            )

    def delete_runs_from(self, run_threshold: int):
        run = Query()
        self.runs.remove(run.run >= run_threshold)
        self.scores.remove(run.run >= run_threshold)
