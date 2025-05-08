import io
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.utils.helpers import format_as_markdown, clean_medical_body
from mars.service.rag_context import app_context
from mars.service.service import (run_baseline,
                                  run_baseline_rag)


router = APIRouter()


@router.post('/api/baseline/base')
async def baseline(payload: QueryRequest) -> JSONResponse:
    res = run_baseline(base_url=payload.base_url,
                       lm_name=payload.lm_name,
                       system_message=payload.system_message,
                       query=payload.query)
    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/baseline/rag')
async def baseline_rag(payload: QueryRequest) -> JSONResponse:
    rag = app_context.rag
    res = run_baseline_rag(base_url=payload.base_url,
                           lm_name=payload.lm_name,
                           system_message=payload.system_message,
                           query=payload.query,
                           rag=rag)
    return JSONResponse({'response': format_as_markdown(res)})


@router.post('/api/baseline/base-docx')
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
        responses.append(res)
    return JSONResponse({'response': format_as_markdown('\n'.join(responses))})


@router.post('/api/baseline/rag-docx')
async def baseline_rag_upload_docx(file: UploadFile = File(...),
                                   base_url: str = Form(...),
                                   lm_name: str = Form(...),
                                   system_message: str = Form(...)) -> JSONResponse:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    text = '\n'.join([para.text for para in doc.paragraphs])
    rag = app_context.rag
    res = run_baseline_rag(base_url=base_url,
                           lm_name=lm_name,
                           system_message=system_message,
                           query=text,
                           rag=rag)
    return JSONResponse({'response': format_as_markdown(res)})
