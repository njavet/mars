from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post('/api/chat')
async def chat(request: Request) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    return JSONResponse({'response': query})
