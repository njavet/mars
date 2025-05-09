# project imports
from mars.schemas import EvalDoc, ScoreEntry
from mars.data.eval_repo import EvalRepository
from mars.service.eval import Evaluator


class MarsService:
    def __init__(self):
        self.eval_repo = EvalRepository()

    def get_runs_list(self) -> list[int]:
        return list(range(self.eval_repo.get_latest_run()))

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        return self.eval_repo.get_eval_docs(run)

    def get_scores(self, run: int) -> list[ScoreEntry]:
        return self.eval_repo.get_scores(run)

    def save_stores(self, scores: list[ScoreEntry]) -> None:
        self.eval_repo.save_scores(scores)
