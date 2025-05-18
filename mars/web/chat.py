import io
from fastapi.responses import JSONResponse
from docx import Document
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Form,
                     Depends)

# project imports
from mars.schema.req import LLMSpec
from mars.schema.llm import Message
from mars.engine.service import run_chat
from mars.core.deps import (get_username, get_chat_repo)


router = APIRouter()
# TODO generate vs chat response format


@router.post('/chat')
async def post_llm_chat(llm_spec: LLMSpec,
                        messages: list[Message],
                        username: str = Depends(get_username),
                        repo = Depends(get_chat_repo)):
    res = run_chat(llm_spec, messages, username, repo)
    return JSONResponse(content=res)


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

