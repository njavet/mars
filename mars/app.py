import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# project imports
from mars import config


def create_fastapi_app():
    app = FastAPI()
    app.mount('/static', StaticFiles(directory='static'), name='static')
    templates = Jinja2Templates(directory='templates')

    @app.get('/', response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse('index.html',
                                          {'request': request})

    @app.post('/chat')
    async def chat(request: Request):
        data = await request.json()
        query = data.get('message')

        # Generate responses
        non_rag_res = app.kai.generate_non_rag_response(query)
        rag_res = app.kai.generate_rag_response(query)
        agentic_rag_res = app.kai.generate_agentic_rag_response(query)

        # Return JSON response with the rendered HTML
        return JSONResponse({'non_rag_response': non_rag_res,
                             'rag_response': rag_res,
                             'agentic_rag_response': agentic_rag_res})

    return app
