import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# project imports
from mars import config
from mars.services.kai_service import MarsService


def create_app():
    app = FastAPI()
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.kai = MarsService(config.ollama_model_name,
                          config.sentence_transformer_name,
                          Path('zhaw_data', 'pdfs'),
                          config.chunk_size)

    templates = Jinja2Templates(directory='templates')

    @app.get('/', response_class=FileResponse)
    async def index():
        return FileResponse('index.html')

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


def run_app():
    uvicorn.run('mars:create_app',
                port=8080,
                reload=True,
                factory=True,
                log_level='debug')

