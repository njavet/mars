import io
import requests
from fastapi import APIRouter, UploadFile, File, Query, Depends
from fastapi.responses import JSONResponse
from docx import Document
from sqlalchemy.orm import Session

# project imports
from mars.schemas import QueryRequest
from mars.utils.prompt import load_preprompts
from mars.service.agent import get_agent
from mars.web.deps import get_db


router = APIRouter()


@router.get('/api/lms')
async def get_lms(base_url: str = Query(...)):
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


@router.get('/api/preprompts')
async def get_preprompts():
    return load_preprompts()


@router.post('/api/chat')
def chat(payload: QueryRequest, session: Session = Depends(get_db)) -> JSONResponse:
    agent = get_agent(payload.lm_name, payload.base_url, payload.enable_rag, session)
    return JSONResponse({'response': agent.run_query(payload.query)})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...),
                      enable_rag: bool = Query(...),
                      lm_name: str = Query(...),
                      base_url: str = Query(...),
                      session: Session = Depends(get_db)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    agent = get_agent(lm_name, base_url, enable_rag, session)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return JSONResponse({'response': agent.run_query(text)})
