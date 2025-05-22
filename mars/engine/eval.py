from collections import defaultdict
from fastapi.logger import logger

# project imports
from mars.conf import DOCX_DIR, SCORE_KEYS, TEXT_DIR
from mars.schema.eval import EvalDoc, ScoreEntry
from mars.schema.llm import Message
from mars.db.eval_repo import EvalRepository
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.parsing import (get_doc_sections,
                                 parse_text_to_llm_input,
                                 unify_small_sections)


class Evaluator:
    def __init__(self,
                 repo: EvalRepository,
                 llms: list[OllamaLLM],
                 base_url: str,
                 system_message: str,
                 chat_api: bool = True,
                 system_message_role: str = 'user'):
        self.repo = repo
        self.llms = llms
        self.base_url = base_url
        self.system_message = parse_text_to_llm_input(system_message)
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
        logger.info(f'starting eval...{run}')
        for text_path in TEXT_DIR.glob('*.txt'):
            logger.info(f'evaluating doc {text_path.name}...')
            with open(text_path) as f:
                text = f.read()
            text = parse_text_to_llm_input(text)
            self.eval_with_scores(run, text_path.name, text)

    def eval_with_scores(self, run: int, filename: str, text: str):
        lms_output, scores = self.eval_doc(run, filename, text)
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
                 text: str) -> tuple[dict[str, str], list[ScoreEntry]]:
        outputs = defaultdict(list)
        scores = []
        for llm in self.llms:
            logger.info(f'running {llm.name}...')
            if self.chat_api:
                messages = [Message(role='system', content=self.system_message),
                            Message(role='user', content=text)]
                res = llm.chat(messages)
            else:
                # TODO implement generate
                res = {}
            outputs[llm.name].append(res)
            score = self.init_scores(run, filename, llm.name)
            scores.append(score)
        lms_output = {lm.name: '\n'.join(outputs[lm.name]) for lm in self.llms}
        return lms_output, scores

    @staticmethod
    def init_scores(run: int, filename: str, lm_name: str) -> ScoreEntry:
        scores = {key: 'undefined' for key in SCORE_KEYS}
        return ScoreEntry(run=run,
                          filename=filename,
                          lm_name=lm_name,
                          scores=scores)
