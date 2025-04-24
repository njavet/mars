import io
from fastapi import APIRouter, Request, UploadFile, File, Query
from fastapi.responses import JSONResponse
from docx import Document

# project imports
from mars.conf import LMS
from mars.schemas.req import QueryRequest
from mars.service.agent import get_agent


router = APIRouter()


@router.get('/api/lms')
async def get_lms(request: Request):
    return LMS


@router.post('/api/chat')
async def chat(payload: QueryRequest) -> JSONResponse:
    agent = get_agent(payload.lm_name, payload.base_url)
    return JSONResponse({'response': agent.run_query(payload.query)})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...),
                      lm_name: str = Query(...),
                      base_url: str = Query(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    agent = get_agent(lm_name, base_url)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return JSONResponse({'response': agent.run_query(text)})
