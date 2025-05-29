import argparse
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from rich.logging import RichHandler
import uvicorn

# project imports
from mars.core.conf import FAST_API_PORT
from mars.core.deps import load_system_messages, get_models
from mars.db.eval_repo import EvalRepository
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.eval import Evaluator
from mars.web import router


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[RichHandler(rich_tracebacks=True,
                          show_time=False)]
)


def create_app():
    app = FastAPI()

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
    repo = EvalRepository()
    # TODO spec llms
    server_models = get_models(args.base_url)
    server_models = ['llama3.1:8b',
                     'openhermes:latest',
                     'dolphin3:latest',
                     'llama3.1:8b-instruct-q6_k']
    server_models = ['mistral:7b-instruct',
                     'llama3.1:8b-instruct-q8_0',
                     'llama3.3:70b',
                     'llama3.3:70b-instruct-q8_0']
    llms = [OllamaLLM(base_url=args.base_url, model=model)
            for model in server_models]
    try:
        system_message = [sm.text for sm in sms if sm.key == args.preprompt][0]
    except KeyError:
        print('No such preprompt')
    else:
        e = Evaluator(repo=repo,
                      llms=llms,
                      base_url=args.base_url,
                      system_message=system_message)
        e.run_eval_from_text()


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--server',
                        dest='base_url',
                        default='http://localhost:11434')
    parser.add_argument('-p',
                        '--preprompt',
                        dest='preprompt',
                        default='medical_json')
    return parser


if __name__ == '__main__':
    run_eval()
