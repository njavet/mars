from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse

# project imports
from mars.core.deps import get_chat_repo, get_username
from mars.engine.service import run_chat
from mars.schema.req import LLMRequest

router = APIRouter()


@router.post("/chat")
async def post_llm_chat(
    llm_req: LLMRequest,
    username: str = Depends(get_username),
    repo=Depends(get_chat_repo),
) -> JSONResponse:
    res = run_chat(llm_req, username, repo)
    return JSONResponse(content=res)


@router.post("/chat/doc")
async def run_doc_query(
    file: UploadFile = File(...),
    base_url: str = Form(...),
    model_name: str = Form(...),
    system_message: str = Form(...),
    agentic: bool = Form(...),
    username: str = Depends(get_username),
    repo=Depends(get_chat_repo),
) -> JSONResponse:
    contents = await file.read()
    llm_req = LLMRequest(
        base_url=base_url,
        model_name=model_name,
        system_message=system_message,
        user_message=contents,
        agentic=agentic,
    )
    res = run_chat(llm_req, username, repo)
    return JSONResponse(content=res)
