import io
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.service.parsing import clean_medical_body
from mars.service.service import run_baseline, run_baseline_rag


router = APIRouter(prefix='/api')
# TODO generate vs chat response format


@router.post('/baseline/base')
async def baseline(payload: QueryRequest) -> JSONResponse:
    res = run_baseline(payload.base_url,
                       payload.lm_name,
                       payload.system_message,
                       payload.query)

    return JSONResponse({'response': res['message']['content']})


@router.post('/baseline/rag')
async def baseline_rag(payload: QueryRequest) -> JSONResponse:
    res = run_baseline_rag(base_url=payload.base_url,
                           lm_name=payload.lm_name,
                           system_message=payload.system_message,
                           query=payload.query)
    return JSONResponse({'response': res['message']['content']})


@router.post('/baseline/base-docx')
async def baseline_upload_docx(file: UploadFile = File(...),
                               base_url: str = Form(...),
                               lm_name: str = Form(...),
                               system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    dix = clean_medical_body(doc)
    responses = []
    for k, v in dix.items():
        res = run_baseline(base_url=base_url,
                           lm_name=lm_name,
                           system_message=system_message,
                           query='\n'.join(v))
        res2 = k.upper() + res['message']['content'] + '\n'
        responses.append(res2)
    return JSONResponse({'response': '\n'.join(responses)})


@router.post('/baseline/rag-docx')
async def baseline_rag_upload_docx(file: UploadFile = File(...),
                                   base_url: str = Form(...),
                                   lm_name: str = Form(...),
                                   system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    dix = clean_medical_body(doc)
    responses = []
    for k, v in dix.items():
        res = run_baseline_rag(base_url=base_url,
                               lm_name=lm_name,
                               system_message=system_message,
                               query='\n'.join(v))
        res2 = k.upper() + res['message']['content'] + '\n'
        responses.append(res2)
    return JSONResponse({'response': '\n'.join(responses)})


@router.post('/baseline/base-text')
async def baseline_upload_text(file: UploadFile = File(...),
                               base_url: str = Form(...),
                               lm_name: str = Form(...),
                               system_message: str = Form(...)) -> JSONResponse:
    content = await file.read()
    text = content.decode('utf-8')
    res = run_baseline(base_url=base_url,
                       lm_name=lm_name,
                       system_message=system_message,
                       query=text)
    return JSONResponse({'response': res['message']['content']})
