from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from rich.logging import RichHandler
import logging
import uvicorn

# project imports
from mars.conf import FAST_API_PORT
from mars.service.bot import Bot
from mars.web import router


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[RichHandler(rich_tracebacks=True,
                          show_time=False)]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.bot = Bot()
    logger.info(f'[MAIN] bot created...')
    yield
    logger.info(f'[MAIN] app shutdown...')


def create_app():
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(CORSMiddleware,
                       allow_origins=['http://localhost:5173'],
                       allow_methods=["*"],
                       allow_headers=["*"],)

    app.include_router(router)

    return app


def run_app():
    uvicorn.run('mars.main:create_app',
                port=FAST_API_PORT,
                reload=True,
                reload_dirs=['mars'],
                factory=True,
                log_level='debug')


if __name__ == '__main__':
    run_app()
