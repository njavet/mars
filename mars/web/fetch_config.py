import subprocess
from fastapi.responses import JSONResponse
from fastapi import (APIRouter, Query)

# project imports
from mars.utils.helpers import load_prompts
from mars.service.service import get_lms


router = APIRouter()


@router.get('/api/username')
async def fetch_username():
    res = subprocess.run(['whoami'])
    print(res)


@router.get('/api/lms')
async def fetch_lms(base_url: str = Query(...)):
    lms = get_lms(base_url)
    return lms


@router.get('/api/system-messages')
async def fetch_system_messages() -> JSONResponse:
    return load_prompts()
