from fastapi import APIRouter, Request

# project imports
from mars.conf import LMS

router = APIRouter()


@router.get('/api/lms')
async def get_lms(request: Request):
    return LMS
