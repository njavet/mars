from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

# project imports
from mars.conf import LLMS

router = APIRouter()


@router.get('/api/lms')
async def get_lms(request: Request):
    return LLMS
