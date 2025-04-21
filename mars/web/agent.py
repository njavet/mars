from fastapi import APIRouter, Request, Response


router = APIRouter()


@router.post('/api/chat')
async def chat(request: Request) -> Response:
    data = await request.json()
    query = data.get('query')
    print(query)
