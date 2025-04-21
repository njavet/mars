from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse
import io
from docx import Document


router = APIRouter()


@router.post('/api/chat')
async def chat(request: Request) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    return JSONResponse({'response': query})


@router.post('/api/upload-docx')
async def upload_docx(file: UploadFile = File(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])

    response = ''
    return JSONResponse({'response': response})
