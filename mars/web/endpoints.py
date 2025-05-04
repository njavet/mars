import io
import requests
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Query,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.utils.prompt import load_prompts
from mars.utils.text_formatters import format_as_markdown
from mars.service.rag_context import app_context
from mars.service.service import run_query


router = APIRouter()


@router.get('/api/lms')
async def get_lms(base_url: str = Query(...)):
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


@router.get('/api/system-messages')
async def get_system_messages() -> JSONResponse:
    return load_prompts()


@router.post('/api/baseline/chat')
async def chat(payload: QueryRequest) -> JSONResponse:
    if payload.enable_rag:
        rag = app_context.rag
        res = run_query(base_url=payload.base_url,
                        lm_name=payload.lm_name,
                        system_message=payload.system_message,
                        query=payload.query,
                        rag=rag)
    else:
        res = run_query(base_url=payload.base_url,
                        lm_name=payload.lm_name,
                        system_message=payload.system_message,
                        query=payload.query)

    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/baseline/upload-docx')
async def upload_docx(file: UploadFile = File(...),
                      base_url: str = Form(...),
                      lm_name: str = Form(...),
                      enable_rag: bool = Form(...),
                      system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])

    if enable_rag:
        rag = app_context.rag
        res = run_query(base_url=base_url,
                        lm_name=lm_name,
                        system_message=system_message,
                        query=text,
                        rag=rag)
    else:
        res = run_query(base_url=base_url,
                        lm_name=lm_name,
                        system_message=system_message,
                        query=text)
    return JSONResponse({'response': res})
