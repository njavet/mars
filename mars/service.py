from fastapi.logger import logger
import requests

# project imports
from mars.conf import EVAL_LMS
from mars.schema.req import LLMRequest
from mars.schemas import EvalDoc, ScoreEntry
from mars.data.eval_repo import EvalRepository
from mars.data.chat_repo import ChatRepository
from mars.engine.ollama_llm import OllamaLLM
from mars.engine.eval import Evaluator
from mars.engine.parsing import parse_text_to_llm_input


def get_models(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    models = [model['name'] for model in data.get('models', [])]
    return models


def run_llm_request(payload: LLMRequest,
                    username: str,
                    repo: ChatRepository) -> str:

    chat = repo.get_chat(username)
    logger.info(f'Running query with {payload.model}')
    llm = OllamaLLM(base_url=payload.base_url, model=payload.model)

    if payload.chat_api:
        system_message = parse_text_to_llm_input(payload.system_message)
        messages = [{'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': payload.user_message}]
        res = llm.chat(messages)
    else:
        # TODO implement generate
        res = {}
    logger.info(f'LLM response generated...')
    return res['message']['content']


class MarsService:
    def __init__(self):
        self.eval_repo = EvalRepository()
        self.chat_repo = ChatRepository()

    def run_eval(self, base_url: str, system_message: str):
        server_lms = get_lm_names(base_url)
        lms = [LanguageModel(name=lm_name, base_url=base_url)
               for lm_name in server_lms if lm_name in EVAL_LMS]
        e = Evaluator(repo=self.eval_repo,
                      lms=lms,
                      base_url=base_url,
                      system_message=system_message)
        e.run_eval_from_text()

    def get_runs_list(self) -> list[int]:
        run = self.eval_repo.get_latest_run()
        return list(range(run))

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        return self.eval_repo.get_eval_docs(run)

    def get_scores(self, run: int) -> list[ScoreEntry]:
        return self.eval_repo.get_scores(run)

    def save_stores(self, scores: list[ScoreEntry]) -> None:
        self.eval_repo.save_scores(scores)



