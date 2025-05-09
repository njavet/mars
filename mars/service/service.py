import requests

# project imports
from mars.schemas import EvalDoc, ScoreEntry
from mars.data.eval_repo import EvalRepository
from mars.service.lm import LanguageModel
from mars.service.eval import Evaluator


class MarsService:
    def __init__(self):
        self.eval_repo = EvalRepository()

    def run_eval(self, base_url: str, system_message: str):
        lms = [LanguageModel(name=lm_name, base_url=base_url)
               for lm_name in get_lm_names(base_url)]
        e = Evaluator(repo=self.eval_repo,
                      lms=lms,
                      base_url=base_url,
                      system_message=system_message)
        e.run_eval()

    def get_runs_list(self) -> list[int]:
        return list(range(self.eval_repo.get_latest_run()))

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        return self.eval_repo.get_eval_docs(run)

    def get_scores(self, run: int) -> list[ScoreEntry]:
        return self.eval_repo.get_scores(run)

    def save_stores(self, scores: list[ScoreEntry]) -> None:
        self.eval_repo.save_scores(scores)


def get_lm_names(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lm_names = [lm_name['name'] for lm_name in data.get('models', [])]
    return lm_names
