from fastapi import APIRouter, Depends

# project imports
from mars.schema.eval import EvalDoc, ScoreEntry
from mars.web.deps import get_eval_repo


router = APIRouter()


@router.get('/runs')
def fetch_runs(repo = Depends(get_eval_repo)):
    run = repo.get_latest_run()
    return list(range(run))


@router.get('/results/{run}')
def fetch_eval_results(run: int, repo = Depends(get_eval_repo)) -> list[EvalDoc]:
    return repo.get_eval_docs(run)


@router.get('/fetch-scores/{run}')
async def fetch_eval_scores(run: int, repo = Depends(get_eval_repo)) -> list[ScoreEntry]:
    return repo.get_scores(run)


@router.post('/save-scores/{run}')
async def save_eval_results(scores: list[ScoreEntry], repo = Depends(get_eval_repo)):
    repo.save_scores(scores)
