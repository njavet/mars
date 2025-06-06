import argparse
import tempfile
import subprocess
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from rich.logging import RichHandler
from jinja2 import Environment, FileSystemLoader
import uvicorn

# project imports
from mars.core.conf import FAST_API_PORT, EVAL_LLMS_CONFIG, EVAL_LLMS_LOCAL
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
    server_models = get_models(args.base_url)
    # server_models = ['llama3.1:8b']
    # server_models = ['deepseek-r1:8b']
    llms = [OllamaLLM(base_url=args.base_url, model_name=model_name)
            for model_name in server_models if model_name in EVAL_LLMS_LOCAL]
    try:
        system_message = [sm.text for sm in sms if sm.key == args.preprompt][0]
    except KeyError:
        print('No such preprompt')
    else:
        e = Evaluator(repo=repo,
                      llms=llms,
                      base_url=args.base_url,
                      system_message=system_message,
                      dtype='markdown',
                      agentic=False)
        e.run_eval()


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--server',
                        dest='base_url',
                        default='http://localhost:11434')
    parser.add_argument('-p',
                        '--preprompt',
                        dest='preprompt',
                        default='baseline')
    return parser


def create_ollama_models(llms=EVAL_LLMS_LOCAL):
    env = Environment(loader=FileSystemLoader('mars/core/'))
    template = env.get_template('Modelfile')
    for model_name in llms:
        rendered = template.render(model_name=model_name,
                                   num_ctx=EVAL_LLMS_CONFIG['num_ctx'],
                                   temperature=EVAL_LLMS_CONFIG['temperature'],
                                   top_k=EVAL_LLMS_CONFIG['top_k'],
                                   top_p=EVAL_LLMS_CONFIG['top_p'])
        with tempfile.NamedTemporaryFile('w+', delete=False) as f:
            f.write(rendered)
            f.flush()
            subprocess.run(['ollama', 'create', '-f', f.name, model_name])


if __name__ == '__main__':
    run_eval()
