import io
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Form)

# project imports
from mars.schemas import QueryRequest
from mars.engine.parsing import (clean_medical_body,
                                 parse_text_to_llm_input,
                                 unify_small_sections)
from mars.mars import MarsService


router = APIRouter()
# TODO generate vs chat response format


@router.post('/chat')
async def run_query(payload: QueryRequest):
    ms = MarsService()
    res = ms.run_query(payload)
    return JSONResponse(content=res['message']['content'])


@router.post('/chat/doc')
async def run_doc_query(file: UploadFile = File(...),
                        base_url: str = Form(...),
                        lm_name: str = Form(...),
                        system_message: str = Form(...),
                        mode: str = Form(...),
                        tools: list[str] = Form(...)) -> JSONResponse:
    ms = MarsService()
    # TODO how to parse docx
    if file.filename.lower().endswith('.docx'):
        contents = await file.read()
        doc = Document(io.BytesIO(contents))
        dix = clean_medical_body(doc)
        for k, v in dix.items():
            responses = []
            qr = QueryRequest(base_url=base_url,
                              lm_name=lm_name,
                              system_message=system_message,
                              query='\n'.join(v),
                              mode=mode,
                              tools=tools)
            res = ms.run_query(qr)
            res2 = k.upper() + res['message']['content'] + '\n'
            responses.append(res2)
            res = JSONResponse({'content': '\n'.join(responses)})
            return res
    elif file.filename.lower().endswith('.txt'):
        contents = await file.read()
        sections = parse_text_to_llm_input(contents).split('\n\n')
        sections = unify_small_sections(sections)
        responses = []
        for section in sections:
            qr = QueryRequest(base_url=base_url,
                              lm_name=lm_name,
                              system_message=system_message,
                              query=section,
                              mode=mode,
                              tools=tools)
            res = ms.run_query(qr)
            res2 = section.upper() + res['message']['content'] + '\n'
            responses.append(res2)
        res = JSONResponse({'content': '\n'.join(responses)})
        return res

