from collections import defaultdict
from docx import Document
from fastapi.logger import logger

# project imports
from mars.conf.conf import DOCX_DIR, SCORE_KEYS
from mars.schemas import EvalDoc, ScoreEntry
from mars.data.eval_repo import EvalRepository
from mars.service.lm import LanguageModel, get_lm_names
from mars.service.parsing import clean_medical_body


class Evaluator:
    def __init__(self,
                 repo: EvalRepository,
                 lms: list[LanguageModel],
                 base_url: str,
                 system_message: str,
                 chat_api: bool = True,
                 system_message_role: str = 'user'):
        self.repo = repo
        self.lms = lms
        self.base_url = base_url
        self.system_message = system_message
        self.chat_api = chat_api
        self.system_message_role = system_message_role

    def run_eval(self):
        run = self.repo.get_latest_run()
        logger.info(f'starting eval...')
        all_scores = []
        for docx_path in DOCX_DIR.glob('*.docx'):
            doc = Document(docx_path)
            logger.info(f'evaluating doc {docx_path.name}...')
            lms_output, scores = self.eval_doc(run, docx_path.name, doc)
            result = EvalDoc(run=run,
                             server=self.base_url,
                             filename=docx_path.name,
                             system_message=self.system_message,
                             chat_api=self.chat_api,
                             system_message_role=self.system_message_role,
                             lms=lms_output)
            self.repo.save_eval_doc(result)
            all_scores.extend(scores)
        self.repo.save_scores(all_scores)

    # TODO refactor scores init
    def eval_doc(self,
                 run: int,
                 filename: str,
                 doc: Document) -> tuple[dict[str, str], list[ScoreEntry]]:
        dix = clean_medical_body(doc)
        outputs = defaultdict(list)
        scores = []
        for lm in self.lms:
            logger.info(f'running {lm.name}...')
            for section, lines in dix.items():
                if self.chat_api:
                    res = lm.chat(system_message=self.system_message,
                                  query='\n'.join(lines),
                                  system_message_role=self.system_message_role)
                else:
                    # TODO implement generate
                    res = {}
                outputs[lm.name].append(res['message']['content'])
            score = self.init_scores(run, filename, lm.name)
            scores.append(score)
        lms_output = {lm.name: '\n'.join(outputs[lm.name]) for lm in self.lms}
        return lms_output, scores

    @staticmethod
    def init_scores(run: int, filename: str, lm_name: str) -> ScoreEntry:
        scores = {key: 'undefined' for key in SCORE_KEYS}
        return ScoreEntry(run=run,
                          filename=filename,
                          lm_name=lm_name,
                          scores=scores)


class EvalCollector:
    def __init__(self):
        self.repo = EvalRepository()

    def get_runs_list(self) -> list[int]:
        return list(range(self.repo.get_latest_run()))

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        return self.repo.get_eval_docs(run)

    def get_scores(self, run: int) -> list[ScoreEntry]:
        return self.repo.get_scores(run)

    def save_stores(self, scores: list[ScoreEntry]) -> None:
        self.repo.save_scores(scores)
