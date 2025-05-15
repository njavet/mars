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
async def run_doc_query(file: UploadFile = File(...),
                        base_url: str = Form(...),
                        lm_name: str = Form(...),
                        system_message: str = Form(...)) -> JSONResponse:
    ms = MarsService()
    if file.filename.lower().endswith('.docx'):
        contents = await file.read()
        doc = Document(io.BytesIO(contents))
        dix = clean_medical_body(doc)
        responses = []
        for k, v in dix.items():
            res = ms.run_query(base_url=base_url,
                               lm_name=lm_name,
                               system_message=system_message,
                               query='\n'.join(v))
            res2 = k.upper() + res['message']['content'] + '\n'
            responses.append(res2)
        res = JSONResponse({'content': '\n'.join(responses)})
        return res
    elif file.filename.lower().endswith('.txt'):
        contents = await file.read()
        print(contents)
        res = JSONResponse({'content': ''})
        return res
