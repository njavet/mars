import subprocess
from fastapi.responses import JSONResponse
from fastapi import (APIRouter, Query)

# project imports
from mars.conf import SERVERS, PORTS
from mars.utils.helpers import load_prompts
from mars.service.service import get_lms


router = APIRouter()


@router.get('/api/servers')
async def fetch_servers():
    res = subprocess.run(['whoami'], capture_output=True, text=True)
    username = res.stdout.strip()
    port = PORTS.get(username, 11434)
    servers = [':'.join([server, port]) for server in SERVERS]
    return JSONResponse(content={'servers': servers})


@router.get('/api/lms')
async def fetch_lms(base_url: str = Query(...)):
    lms = get_lms(base_url)
    return lms


@router.get('/api/system-messages')
async def fetch_system_messages() -> JSONResponse:
    return load_prompts()
