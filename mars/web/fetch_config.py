import subprocess
from fastapi.responses import JSONResponse
from fastapi import (APIRouter, Query)

# project imports
from mars.conf.conf import SERVERS, PORTS, OP_MODES
from mars.utils.helpers import load_system_messages
from mars.schemas import SystemMessage
from mars.service.service import get_lm_names

# TODO base api router prefix
router = APIRouter()


@router.get('/api/servers')
async def fetch_servers():
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    port = PORTS.get(username, 11434)
    servers = [':'.join([server, str(port)]) for server in SERVERS]
    return JSONResponse(content={'servers': servers})


@router.get('/api/lms')
async def fetch_lms(base_url: str = Query(...)):
    lms = get_lm_names(base_url)
    return lms


@router.get('/api/system-messages')
async def fetch_system_messages() -> list[SystemMessage]:
    sys_msg = load_system_messages()
    return sys_msg


@router.get('/api/op-modes')
async def get_operation_modes() -> list[str]:
    return OP_MODES
