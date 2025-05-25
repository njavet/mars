import subprocess
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query

# project imports
from mars.core.conf import SERVERS, PORTS, LIBS
from mars.utils.helpers import load_system_messages
from mars.schema.res import SystemMessage
from mars.engine.service import get_models


router = APIRouter()


@router.get('/servers')
async def fetch_servers():
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    port = PORTS.get(username, 11434)
    servers = [':'.join([server, str(port)]) for server in SERVERS]
    return JSONResponse(content={'servers': servers})


@router.get('/models')
async def fetch_models(base_url: str = Query(...)):
    models = get_models(base_url)
    return models


@router.get('/system-messages')
async def fetch_system_messages() -> list[SystemMessage]:
    sys_msg = load_system_messages()
    return sys_msg


@router.get('/libs')
async def fetch_libs() -> list[str]:
    return LIBS
