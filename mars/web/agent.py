from fastapi import APIRouter, Request, UploadFile, File, Query
from fastapi.responses import JSONResponse
import io
from docx import Document

# project imports
from mars.service.agent import LMAgentService

router = APIRouter()


@router.post('/api/chat')
async def chat(request: Request, lm_name: str = Query(...)) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    service = LMAgentService(lm_name)
    return JSONResponse({'response': query})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])
    response = ''
    return JSONResponse({'response': response})
