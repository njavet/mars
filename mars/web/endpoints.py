import io
import json
import os
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Request,
                     Query,
                     Form)

# project imports
from mars.conf import RESULTS_DIR
from mars.schemas import QueryRequest
from mars.utils.helpers import load_prompts
from mars.utils.helpers import format_as_markdown
from mars.service.rag_context import app_context
from mars.service.service import (get_lms,
                                  run_baseline,
                                  run_baseline_rag)


router = APIRouter()



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

