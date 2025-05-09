from fastapi import APIRouter, HTTPException

# project imports
from mars.schemas import EvalDoc, ScoreEntry
from mars.service.eval import EvalCollector


router = APIRouter()


@router.get('/api/runs')
def fetch_runs():
    ec = EvalCollector()
    return ec.get_runs_list()


@router.get('/api/results/{run}')
def fetch_eval_results(run: int) -> list[EvalDoc]:
    ec = EvalCollector()
    return ec.get_eval_docs(run)


@router.get('/api/fetch-scores/{run}')
async def fetch_eval_scores(run: int):
    ec = EvalCollector()
    return ec.get_scores(run)


@router.post('/api/save-scores/{run}')
async def save_eval_results(scores: list[ScoreEntry]):
    ec = EvalCollector()
    ec.save_stores(scores)
