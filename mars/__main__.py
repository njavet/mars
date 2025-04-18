import uvicorn

# project imports
from . import create_fastapi_app


uvicorn.run('mars:create_fastapi_app',
            port=8080,
            reload=True,
            factory=True,
            log_level='debug')
