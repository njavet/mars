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
from mars.service.service import (run_baseline,
                                  run_baseline_rag)


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


@router.post('/api/baseline/base')
async def baseline(payload: QueryRequest) -> JSONResponse:
    res = run_baseline(base_url=payload.base_url,
                       lm_name=payload.lm_name,
                       system_message=payload.system_message,
                       query=payload.query)
    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/baseline/rag')
async def baseline_rag(payload: QueryRequest) -> JSONResponse:
    rag = app_context.rag
    res = run_baseline_rag(base_url=payload.base_url,
                           lm_name=payload.lm_name,
                           system_message=payload.system_message,
                           query=payload.query,
                           rag=rag)
    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/baseline/base-docx')
async def upload_docx(file: UploadFile = File(...),
                      base_url: str = Form(...),
                      lm_name: str = Form(...),
                      system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])
    res = run_baseline(base_url=base_url,
                       lm_name=lm_name,
                       system_message=system_message,
                       query=text)
    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/baseline/rag-docx')
async def upload_docx(file: UploadFile = File(...),
                      base_url: str = Form(...),
                      lm_name: str = Form(...),
                      system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])
    rag = app_context.rag
    res = run_baseline_rag(base_url=base_url,
                           lm_name=lm_name,
                           system_message=system_message,
                           query=text,
                           rag=rag)
    return JSONResponse({'response': format_as_markdown(res)})
