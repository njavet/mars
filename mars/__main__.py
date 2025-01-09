import uvicorn


uvicorn.run('mars:create_app',
            port=8080,
            reload=True,
            factory=True,
            log_level='debug')

