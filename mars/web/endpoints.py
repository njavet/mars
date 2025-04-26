import io
import requests
from fastapi.responses import JSONResponse
from docx import Document
from sqlalchemy.orm import Session
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Query,
                     Depends,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.utils.prompt import load_prompts
from mars.service.service import get_agent
from mars.web.deps import get_db


router = APIRouter()


@router.get('/api/lms')
async def get_lms(base_url: str = Query(...)):
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


@router.get('/api/system-messages')
async def get_system_messages():
    return load_prompts()


@router.post('/api/chat')
async def chat(payload: QueryRequest, session: Session = Depends(get_db)) -> JSONResponse:
    agent = get_agent(payload.base_url,
                      payload.lm_name,
                      session)
    res = agent.run_query(payload.enable_rag, payload.preprompt, payload.query)
    return JSONResponse({'response': res})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...),
                      base_url: str = Form(...),
                      lm_name: str = Form(...),
                      enable_rag: bool = Form(...),
                      preprompt: str = Form(...),
                      session: Session = Depends(get_db)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    agent = get_agent(base_url, lm_name, session)
    text = '\n'.join([para.text for para in doc.paragraphs])
    res = agent.run_query(enable_rag, preprompt, text)
    return JSONResponse({'response': res})
