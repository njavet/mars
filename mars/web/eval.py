import json
import os
from fastapi import APIRouter, Request, HTTPException

# project imports
from mars.conf.conf import RESULTS_DIR


router = APIRouter()


@router.get('/api/results/{run}')
def fetch_eval_results(run: int):
    run_dir = RESULTS_DIR / f'run{run}'
    if not run_dir.exists() or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail='Run not found')

    results = []
    for file in run_dir.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results.append({
                'lm_name': data.get('lm_name'),
                'output': data.get('output')
            })
    return results


@router.post("/api/save-scores")
async def save_scores(req: Request):
    data = await req.json()
    file = data['file']
    lm_name = data['lm_name']
    scores = data['scores']

    path = f"frontend/public/results/{file}"
    print(f"saving scores to {path}")
    if not os.path.exists(path):
        return {"error": "File not found"}

    with open(path) as f:
        entries = json.load(f)

    for entry in entries:
        if entry["lm_name"] == lm_name:
            entry["scores"] = scores
            break

    with open(path, "w") as f:
        json.dump(entries, f, indent=2)

    return {"status": "ok"}

