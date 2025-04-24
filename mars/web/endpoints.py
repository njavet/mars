from fastapi import APIRouter, Request, UploadFile, File, Query
from fastapi.responses import JSONResponse
import io
from docx import Document

# project imports
from mars.conf import LMS


router = APIRouter()


@router.get('/api/lms')
async def get_lms(request: Request):
    return LMS


@router.post('/api/chat')
async def chat(request: Request, lm_name: str = Query(...)) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    service = LMAgentService(lm_name, 'http://localhost:11434')
    return JSONResponse({'response': service.handle_query(query)})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...),
                      lm_name: str = Query(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])
    service = LMAgentService(lm_name, 'http://localhost:11434')
    return JSONResponse({'response': service.handle_query(text)})

