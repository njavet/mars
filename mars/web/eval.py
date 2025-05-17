from fastapi import APIRouter

# project imports
from mars.schemas import EvalDoc, ScoreEntry
from mars.mars import MarsService


router = APIRouter()


@router.get('/runs')
def fetch_runs():
    ms = MarsService()
    return ms.get_runs_list()


@router.get('/results/{run}')
def fetch_eval_results(run: int) -> list[EvalDoc]:
    ms = MarsService()
    return ms.get_eval_docs(run)


@router.get('/fetch-scores/{run}')
async def fetch_eval_scores(run: int) -> list[ScoreEntry]:
    ms = MarsService()
    return ms.get_scores(run)


@router.post('/save-scores/{run}')
async def save_eval_results(scores: list[ScoreEntry]):
    ms = MarsService()
    ms.save_stores(scores)
