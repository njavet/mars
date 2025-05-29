from fastapi.responses import JSONResponse
from fastapi import (APIRouter,
                     UploadFile,
                     File,
                     Form,
                     Depends)

# project imports
from mars.core.deps import get_username, get_chat_repo
from mars.schema.req import LLMRequest
from mars.engine.service import run_chat


router = APIRouter()


@router.post('/chat')
async def post_llm_chat(llm_req: LLMRequest,
                        username: str = Depends(get_username),
                        repo = Depends(get_chat_repo)):
    res = run_chat(llm_req, username, repo)
    return JSONResponse(content=res)


@router.post('/chat/doc')
async def run_doc_query(file: UploadFile = File(...),
                        base_url: str = Form(...),
                        model_name: str = Form(...),
                        system_message: str = Form(...),
                        agentic: bool = Form(...)):
    contents = await file.read()
