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
async def run_query(payload: QueryRequest,
                    file: Optional[UploadFile] = File(None)):
    ms = MarsService()
    if file and file.filename.lower().endswith('.docx'):
        contents = await file.read()
        doc = Document(io.BytesIO(contents))
        dix = clean_medical_body(doc)
        res = None
    elif file and file.filename.lower().endswith('.txt'):
        res = None
        pass
    else:
        res = ms.run_query(payload)
    return res['message']['content']
