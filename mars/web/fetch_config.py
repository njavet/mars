import subprocess
from fastapi.responses import JSONResponse
from fastapi import (APIRouter, Query)

# project imports
from mars.conf import SERVERS, PORTS, OP_MODES, TOOLS
from mars.utils.helpers import load_system_messages
from mars.schemas import SystemMessage
from mars.mars import get_lm_names


router = APIRouter()


@router.get('/servers')
async def fetch_servers():
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    port = PORTS.get(username, 11434)
    servers = [':'.join([server, str(port)]) for server in SERVERS]
    return JSONResponse(content={'servers': servers})


@router.get('/lms')
async def fetch_lms(base_url: str = Query(...)):
    lms = get_lm_names(base_url)
    return lms


@router.get('/system-messages')
async def fetch_system_messages() -> list[SystemMessage]:
    sys_msg = load_system_messages()
    return sys_msg


@router.get('/op-modes')
async def get_operation_modes() -> dict[str, str]:
    return OP_MODES


@router.get('/tools')
async def get_tools() -> dict[str, str]:
    return TOOLS
