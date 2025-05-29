from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

# project imports
from mars.core.conf import OLLAMA_SERVERS, PORTS, LIBS
from mars.core.deps import get_username, get_models, load_system_messages
from mars.schema.res import SystemMessage


router = APIRouter()


@router.get('/ollama-servers')
async def fetch_ollama_servers(username: str = Depends(get_username)):
    port = PORTS.get(username, 11434)
    ollama_servers = [':'.join([server, str(port)]) for server in OLLAMA_SERVERS]
    return JSONResponse(content={'ollama_servers': ollama_servers})


@router.get('/ollama-models')
async def fetch_ollama_models(base_url: str = Query(...)):
    models = get_models(base_url)
    return models


@router.get('/system-messages')
async def fetch_system_messages() -> list[SystemMessage]:
    sys_msg = load_system_messages()
    return sys_msg


@router.get('/libs')
async def fetch_libs() -> list[str]:
    return LIBS
