import re
from fastapi.logger import logger
import json
from docx import Document

# project imports
from mars.core.conf import SCORE_KEYS, MD_DIR, TEXT_DIR, DOCX_DIR
from mars.schema.eval import EvalDoc, ScoreEntry, Message
from mars.db.eval_repo import EvalRepository
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.parsing import parse_text_to_llm_input
from mars.engine.tools import extract_section_content, justify_missing_section


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
        self.run = self.repo.get_latest_run()

    def run_eval_from_docx(self):
        logger.info(f'starting eval...{self.run}')
        for file_path in DOCX_DIR.glob('*.docx'):
            logger.debug(f'evaluating doc {file_path.name}...')
            doc = Document(file_path)
            text = '\n'.join(
                para.text for para in doc.paragraphs if para.text.strip())
            text = parse_text_to_llm_input(text)
            self.eval_with_scores(file_path.name, text)

    def run_eval_from_markdown(self):
        logger.info(f'starting eval...{self.run}')
        for text_path in MD_DIR.glob('*.md'):
            logger.debug(f'evaluating doc {text_path.name}...')
            with open(text_path) as f:
                text = f.read()
            text = parse_text_to_llm_input(text)
            self.eval_with_scores(text_path.name, text)

    def run_eval_from_markdown_agentic(self):
        logger.info(f'starting eval...{self.run}')
        for text_path in MD_DIR.glob('*.md'):
            logger.info(f'evaluating doc {text_path.name}...')
            with open(text_path) as f:
                text = f.read()
            text = parse_text_to_llm_input(text)
            self.eval_with_scores(text_path.name, text, agentic=True)

    def run_eval_from_text(self):
        logger.info(f'starting eval...{self.run}')
        for text_path in TEXT_DIR.glob('*.txt'):
            logger.info(f'evaluating doc {text_path.name}...')
            with open(text_path) as f:
                text = f.read()
            text = parse_text_to_llm_input(text)
            self.eval_with_scores(text_path.name, text)

    def eval_with_scores(self, filename: str, text: str, agentic: bool = False):
        lms_output, scores = self.eval_doc(filename, text, agentic)
        result = EvalDoc(run=self.run,
                         server=self.base_url,
                         filename=filename,
                         system_message=self.system_message,
                         models=lms_output)
        self.repo.save_eval_doc(result)
        self.repo.save_scores(scores)

    def eval_doc(self,
                 filename: str,
                 text: str,
                 agentic: bool = False) -> tuple[dict[str, str], list[ScoreEntry]]:
        outputs = {}
        scores = []
        for llm in self.llms:
            logger.info(f'running {llm.name}...')
            messages = [Message(role='system', content=self.system_message),
                        Message(role='user', content=text)]
            if agentic:
                res = self.agentic_eval(text, llm, messages)
            else:
                res = llm.chat(messages)

            outputs[llm.name] = res
            score = self.init_scores(filename, llm.name)
            scores.append(score)
        logger.info(f'\n--->>> EVAL DONE FOR DOC {filename}...\n')
        return outputs, scores

    def agentic_eval(self, text, llm, messages: list[Message]) -> str:
        res = llm.chat(messages)
        try:
            dix = json.loads(res)
        except json.decoder.JSONDecodeError:
            print('llm did not return a JSON object')
            return res
        completes = {}
        justified = {}
        for section, score in dix.items():
            if score == 1:
                completes[section] = 1
            else:
                content = extract_section_content(text, section)
                print('content', content)
                justification = justify_missing_section(llm, content)
                justified[section] = justification
        completes_text = '\n'.join([k + ':' + str(v) for k, v in completes.items()])
        just_text = '\n'.join([k + ':' + j for k, j in justified.items()])
        return '\n\n'.join([completes_text, just_text])


    def init_scores(self, filename: str, model_name: str) -> ScoreEntry:
        scores = {key: -1 for key in SCORE_KEYS}
        return ScoreEntry(run=self.run,
                          filename=filename,
                          model_name=model_name,
                          scores=scores)
