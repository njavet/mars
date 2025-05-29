from collections import defaultdict
from fastapi.logger import logger

# project imports
from mars.core.conf import SCORE_KEYS, TEXT_DIR
from mars.schema.eval import EvalDoc, ScoreEntry, Message
from mars.db.eval_repo import EvalRepository
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.parsing import parse_text_to_llm_input, parse_all_json_sections


class Evaluator:
    def __init__(self,
                 repo: EvalRepository,
                 llms: list[OllamaLLM],
                 base_url: str,
                 system_message: str):
        self.repo = repo
        self.llms = llms
        self.base_url = base_url
        self.system_message = parse_text_to_llm_input(system_message)

    def run_eval_from_json(self):
        run = self.repo.get_latest_run()
        logger.info(f'starting eval...{run}')
        sections = parse_all_json_sections(TEXT_DIR)
        lst = []
        dix = defaultdict(list)
        for section in sections:
            dix[section['file']].append('\n'.join(['<section name>',
                                                   section['section'],
                                                   'section content',
                                                   section['content']]))
        for fname, section in dix.items():
            self.eval_with_scores(run, fname, sections)

    def run_eval_from_text(self):
        # TODO refactor
        run = self.repo.get_latest_run()
        logger.info(f'starting eval...{run}')
        for text_path in TEXT_DIR.glob('md_splits/ge_*.md'):
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
                         models=lms_output)
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
            llm_res = []
            messages = [Message(role='system', content=self.system_message),
                        Message(role='user', content=text)]
            res = llm.chat(messages)
            outputs[llm.name].append(res)
            score = self.init_scores(run, filename, llm.name)
            scores.append(score)
        logger.info(f'\n--->>> EVAL DONE FOR DOC {filename}...\n')
        lms_output = {lm.name: '\n'.join(outputs[lm.name]) for lm in self.llms}
        return lms_output, scores

    @staticmethod
    def init_scores(run: int, filename: str, model_name: str) -> ScoreEntry:
        scores = {key: 'undefined' for key in SCORE_KEYS}
        return ScoreEntry(run=run,
                          filename=filename,
                          model_name=model_name,
                          scores=scores)
