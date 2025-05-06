import json
import os
from fastapi import (APIRouter,
                     Request)

# project imports
from mars.conf.conf import RESULTS_DIR


router = APIRouter()


@router.get('/api/results/file-list')
def fetch_eval_results():
    files = os.listdir(RESULTS_DIR)
    return files


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

