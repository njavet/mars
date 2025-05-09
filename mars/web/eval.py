import json
import os
from fastapi import APIRouter, HTTPException

# project imports
from mars.conf.conf import RESULTS_DIR
from mars.schemas import Evaluation, ScoreEntry
from mars.utils.helpers import get_number_of_runs


router = APIRouter()


@router.get('/api/runs')
def fetch_runs():
    return list(range(get_number_of_runs()))


@router.get('/api/results/{run}')
def fetch_eval_results(run: int) -> list[Evaluation]:
    run_dir = RESULTS_DIR / f'run{run}'
    if not run_dir.exists() or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail='Run not found')

    results = []
    for file in run_dir.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            eval_res = Evaluation(**data)
            results.append(eval_res)
    return results


@router.post("/api/save-scores")
async def save_scores(entries: list[ScoreEntry]):
    for entry in entries:
        print('storing', entry.run, entry.filename, entry.lm_name, entry.scores)

    return {"status": "ok"}
