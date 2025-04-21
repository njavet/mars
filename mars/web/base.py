import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



    @app.post('/chat')
    async def chat(request: Request):
        data = await request.json()
        query = data.get('message')

        # Generate responses
        base_res = extract_json(app.baseline.run_query(query).content)
        try:
            agentic_res = extract_json(app.agentic.run_query(query).content)
        except Exception as e:
            agentic_res = {'answer': 'fail', 'source': 'fail', 'page': ''}
            print('EXCEPTION', e)

        #agentic_res = {'answer': 'fail', 'source': 'fail', 'page': ''}
        # Return JSON response with the rendered HTML
        return JSONResponse({'base_res': {'answer': base_res['answer'],
                                          'source': base_res['source'],
                                          'page': base_res['page']},
                             'agentic_res': {'answer': agentic_res['answer'],
                                             'source': agentic_res['source'],
                                             'page': agentic_res['page']}})

