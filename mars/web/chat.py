import io
from typing import Optional
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.service.parsing import clean_medical_body
from mars.service.service import MarsService


router = APIRouter()
# TODO generate vs chat response format


@router.post('/chat')
async def run_query(payload: QueryRequest):
    ms = MarsService()
    res = ms.run_query(payload)
    print(res['message']['content'])
    return JSONResponse(content=res['message']['content'])


@router.post('/chat/doc')
async def run_doc_query(file: UploadFile = File(...)):
    ms = MarsService()
    if file.filename.lower().endswith('.docx'):
        contents = await file.read()
        doc = Document(io.BytesIO(contents))

    elif file.filename.lower().endswith('.txt'):
        contents = await file.read()
        print(contents)
