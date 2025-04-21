from fastapi import APIRouter, Request, Response


router = APIRouter()


@router.get('/api/chat')
def chat(request: Request) -> Response:
    pass
