from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get('/api/lms')
async def get_lms(request: Request):
    data = await request.json()
    query = data.get('query')
    return JSONResponse({'response': query})


