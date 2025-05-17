import argparse
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from starlette.middleware.cors import CORSMiddleware
from rich.logging import RichHandler
import uvicorn

# project imports
from mars.conf import SENTENCE_TRANSFORMER_NAME, FAST_API_PORT
from mars.utils.helpers import load_system_messages
from mars.data.conn import SessionFactory
from mars.data.faiss_repo import FaissRepository
from mars.data.sql_repo import SqlRepository
from mars.engine.rag import RAG
from mars.mars import MarsService, app_context
from mars.web.api import router


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[RichHandler(rich_tracebacks=True,
                          show_time=False)]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_factory = SessionFactory()
    st_model = SentenceTransformer(SENTENCE_TRANSFORMER_NAME)
    faiss_repo = FaissRepository(dim=st_model.get_sentence_embedding_dimension())
    sql_repo = SqlRepository(session_factory=session_factory, faiss_repo=faiss_repo)
    app_context.rag = RAG(st_model, sql_repo)
    yield
    app_context.rag = None


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


def run_eval():
    parser = create_argparser()
    args = parser.parse_args()

    sms = load_system_messages()
    try:
        system_message = [sm.text for sm in sms if sm.key == args.preprompt][0]
    except KeyError:
        print('No such preprompt')
    else:
        ms = MarsService()
        ms.run_eval(base_url=args.base_url,
                    system_message=system_message)


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--server',
                        dest='base_url',
                        default='http://localhost:11434')
    parser.add_argument('-p',
                        '--preprompt',
                        dest='preprompt',
                        default='medical_analyst_binary_2')
    return parser


if __name__ == '__main__':
    run_eval()
