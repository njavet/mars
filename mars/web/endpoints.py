import io
import requests
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     Depends,
                     File,
                     Query,
                     Request,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.utils.prompt import load_prompts
from mars.utils.text_formatters import format_as_markdown
from mars.service.rag import RAG
from mars.web.deps import get_rag


router = APIRouter()


@router.get('/api/lms')
async def get_lms(base_url: str = Query(...)) -> JSONResponse:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


@router.get('/api/system-messages')
async def get_system_messages() -> JSONResponse:
    return load_prompts()


@router.post('/api/chat')
async def chat(payload: QueryRequest, rag: RAG = Depends(get_rag)) -> JSONResponse:
    res = request.app.state.bot.handle_query(payload.base_url,
                                             payload.lm_name,
                                             payload.agent_type,
                                             payload.system_message,
                                             payload.query)
    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/upload-docx')
async def upload_docx(request: Request,
                      file: UploadFile = File(...),
                      base_url: str = Form(...),
                      lm_name: str = Form(...),
                      agent_type: str = Form(...),
                      system_message: str = Form(...),
                      rag: RAG = Depends(get_rag)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])

    res = request.app.state.bot.handle_query(base_url,
                                             lm_name,
                                             agent_type,
                                             system_message,
                                             text)
    return JSONResponse({'response': res})
