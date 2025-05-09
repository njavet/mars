from fastapi.logger import logger
import requests

# project imports
from mars.schemas import EvalDoc, ScoreEntry
from mars.data.eval_repo import EvalRepository
from mars.data.chat_repo import ChatRepository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG
from mars.service.eval import Evaluator


class AppContext:
    rag: RAG | None = None


app_context = AppContext()


class MarsService:
    def __init__(self):
        self.eval_repo = EvalRepository()
        self.chat_repo = ChatRepository()

    def run_eval(self, base_url: str, system_message: str):
        lms = [LanguageModel(name=lm_name, base_url=base_url)
               for lm_name in get_lm_names(base_url)]
        e = Evaluator(repo=self.eval_repo,
                      lms=lms,
                      base_url=base_url,
                      system_message=system_message)
        e.run_eval()

    def get_runs_list(self) -> list[int]:
        return list(range(self.eval_repo.get_latest_run()))

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        return self.eval_repo.get_eval_docs(run)

    def get_scores(self, run: int) -> list[ScoreEntry]:
        return self.eval_repo.get_scores(run)

    def save_stores(self, scores: list[ScoreEntry]) -> None:
        self.eval_repo.save_scores(scores)


def get_lm_names(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lm_names = [lm_name['name'] for lm_name in data.get('models', [])]
    return lm_names


def run_baseline(base_url: str,
                 lm_name: str,
                 system_message: str,
                 query: str,
                 chat_api: bool = True,
                 system_message_role: str = 'user') -> dict:
    logger.info(f'[Baseline] Running query with {lm_name}')
    lm = LanguageModel(name=lm_name, base_url=base_url)
    if chat_api:
        res = lm.chat(system_message=system_message,
                      query=query,
                      system_message_role=system_message_role)
    else:
        # TODO implement generate
        res = {}
    logger.info(f'[Baseline] LLM response generated...')
    return res


def run_baseline_rag(base_url: str,
                     lm_name: str,
                     system_message: str,
                     query: str,
                     chat_api: bool = True,
                     system_message_role: str = 'user') -> dict:
    logger.info(f'[Baseline RAG] Running query with {lm_name}')
    docs = app_context.rag.retrieve_documents(query)
    logger.info(f'[Baseline RAG] Retrieved docs...')
    doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
    system_message = '\n'.join([system_message, doc_msg])
    res = run_baseline(base_url=base_url,
                       lm_name=lm_name,
                       system_message=system_message,
                       query=query,
                       chat_api=chat_api,
                       system_message_role=system_message_role)
    logger.info(f'[Baseline RAG] LLM response generated...')
    return res

