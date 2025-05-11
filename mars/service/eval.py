from collections import defaultdict
from docx import Document
from fastapi.logger import logger

# project imports
from mars.conf.conf import DOCX_DIR, SCORE_KEYS, TEXT_DIR
from mars.schemas import EvalDoc, ScoreEntry
from mars.data.eval_repo import EvalRepository
from mars.service.lm import LanguageModel
from mars.service.parsing import get_doc_sections, parse_text_to_llm_input


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

    def run_eval_from_docx(self):
        run = self.repo.get_latest_run()
        logger.info(f'starting eval...')
        for docx_path in DOCX_DIR.glob('*.docx'):
            logger.info(f'evaluating doc {docx_path.name}...')
            sections = get_doc_sections(docx_path)
            self.eval_with_scores(run, docx_path.name, sections)

    def run_eval_from_text(self):
        # TODO refactor
        run = self.repo.get_latest_run()
        logger.info(f'starting eval...')
        for text_path in TEXT_DIR.glob('*.txt'):
            logger.info(f'evaluating doc {text_path.name}...')
            with open(text_path) as f:
                text = f.read()
            sections = parse_text_to_llm_input(text).split('\n\n')
            self.eval_with_scores(run, text_path.name, sections)

    def eval_with_scores(self, run: int, filename: str, sections: list[str]):
        lms_output, scores = self.eval_doc(run, filename, sections)
        result = EvalDoc(run=run,
                         server=self.base_url,
                         filename=filename,
                         system_message=self.system_message,
                         chat_api=self.chat_api,
                         system_message_role=self.system_message_role,
                         lms=lms_output)
        self.repo.save_eval_doc(result)
        self.repo.save_scores(scores)

    def eval_doc(self,
                 run: int,
                 filename: str,
                 sections: list[str]) -> tuple[dict[str, str], list[ScoreEntry]]:
        outputs = defaultdict(list)
        scores = []
        for lm in self.lms:
            logger.info(f'running {lm.name}...')
            for section in sections:
                if self.chat_api:
                    res = lm.chat(system_message=self.system_message,
                                  query=section,
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
