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


@router.post("/api/save-scores")
async def save_scores(entries: list[ScoreEntry]):
    for entry in entries:
        print('storing', entry.run, entry.filename, entry.lm_name, entry.scores)

    return {"status": "ok"}
