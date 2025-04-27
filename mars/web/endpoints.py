import io
import requests
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Query,
                     Request,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.utils.prompt import load_prompts
from mars.service.service import get_agent


router = APIRouter()


@router.get('/api/lms')
async def get_lms(base_url: str = Query(...)) -> JSONResponse:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


@router.get('/api/system-messages')
async def get_system_messages(request: Request) -> JSONResponse:
    request.app.state.bot.yo()
    return load_prompts()


@router.post('/api/chat')
async def chat(request: Request, payload: QueryRequest) -> JSONResponse:
    session = request.app.state.bot.sf.get_session()
    agent = get_agent(payload.base_url,
                      payload.lm_name,
                      session
                      )
    res = agent.run_query(payload.enable_rag, payload.system_message, payload.query)
    return JSONResponse({'response': res})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...),
                      base_url: str = Form(...),
                      lm_name: str = Form(...),
                      enable_rag: bool = Form(...),
                      system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    agent = get_agent(base_url, lm_name, session)
    text = '\n'.join([para.text for para in doc.paragraphs])
    res = agent.run_query(enable_rag, system_message, text)
    return JSONResponse({'response': res})
