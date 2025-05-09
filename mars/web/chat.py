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
from mars.service.rag_context import app_context
from mars.service.chat import ChatService


router = APIRouter()
# TODO generate vs chat response format


@router.post('/api/baseline/base')
async def baseline(payload: QueryRequest) -> JSONResponse:
    cs = ChatService(base_url=payload.base_url,
                     lm_name=payload.lm_name)
    res = cs.run_baseline(payload.system_message,
                          payload.query)
    return JSONResponse({'response': res['message']['content']})


@router.post('/api/baseline/rag')
async def baseline_rag(payload: QueryRequest) -> JSONResponse:
    cs = ChatService(base_url=payload.base_url,
                     lm_name=payload.lm_name)
    rag = app_context.rag
    res = cs.run_baseline_rag(system_message=payload.system_message,
                              query=payload.query,
                              rag=rag)
    return JSONResponse({'response': res['message']['content']})


@router.post('/api/baseline/base-docx')
async def baseline_upload_docx(file: UploadFile = File(...),
                               base_url: str = Form(...),
                               lm_name: str = Form(...),
                               system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    dix = clean_medical_body(doc)
    cs = ChatService(base_url=base_url,
                     lm_name=lm_name)
    responses = []
    for k, v in dix.items():
        res = cs.run_baseline(system_message=system_message,
                              query='\n'.join(v))
        res2 = k.upper() + res['message']['content'] + '\n'
        responses.append(res2)
    return JSONResponse({'response': '\n'.join(responses)})


@router.post('/api/baseline/rag-docx')
async def baseline_rag_upload_docx(file: UploadFile = File(...),
                                   base_url: str = Form(...),
                                   lm_name: str = Form(...),
                                   system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    dix = clean_medical_body(doc)
    cs = ChatService(base_url=base_url,
                     lm_name=lm_name)
    rag = app_context.rag
    responses = []
    for k, v in dix.items():
        res = cs.run_baseline_rag(system_message=system_message,
                                  query='\n'.join(v),
                                  rag=rag)
        res2 = k.upper() + res['message']['content'] + '\n'
        responses.append(res2)
    return JSONResponse({'response': '\n'.join(responses)})


@router.post('/api/baseline/base-text')
async def baseline_upload_text(file: UploadFile = File(...),
                               base_url: str = Form(...),
                               lm_name: str = Form(...),
                               system_message: str = Form(...)) -> JSONResponse:
    content = await file.read()
    text = content.decode('utf-8')
    cs = ChatService(base_url=base_url,
                     lm_name=lm_name)
    res = cs.run_baseline(system_message=system_message,
                          query=text)
    return JSONResponse({'response': res['message']['content']})
