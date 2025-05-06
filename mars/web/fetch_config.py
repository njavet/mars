import os
from fastapi.responses import JSONResponse
from fastapi import (APIRouter, Query)

# project imports
from mars.conf import RESULTS_DIR
from mars.utils.helpers import load_prompts
from mars.service.service import get_lms


router = APIRouter()


@router.get('/api/lms')
async def fetch_lms(base_url: str = Query(...)):
    lms = get_lms(base_url)
    return lms


@router.get('/api/system-messages')
async def fetch_system_messages() -> JSONResponse:
    return load_prompts()


@router.get('/api/results/file-list')
def fetch_eval_results():
    files = os.listdir(RESULTS_DIR)
    return files
