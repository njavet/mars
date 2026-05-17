from fastapi import APIRouter, Depends

from mars.core.deps import get_eval_repo
from mars.db.eval_repo import EvalRepository

# project imports
from mars.schema.eval import EvalDoc, ScoreEntry

router = APIRouter()


@router.get("/runs")
def fetch_runs(repo: EvalRepository = Depends(get_eval_repo)) -> list[int]:
    run = repo.get_latest_run()
    return list(range(run))


@router.get("/results/{run}")
def fetch_eval_results(
    run: int, repo: EvalRepository = Depends(get_eval_repo)
) -> list[EvalDoc]:
    return repo.get_eval_docs(run)


@router.get("/scores/{run}")
async def fetch_eval_scores(
    run: int, repo: EvalRepository = Depends(get_eval_repo)
) -> list[ScoreEntry]:
    return repo.get_scores(run)


@router.post("/save-scores/{run}")
async def save_eval_results(
    scores: list[ScoreEntry], repo: EvalRepository = Depends(get_eval_repo)
) -> None:
    repo.save_scores(scores)
