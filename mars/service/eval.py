from pathlib import Path
from docx import Document

# project imports
from mars.conf.conf import DOCX_DIR
from mars.data.tables import (EvaluationDocument,
                              EvaluationResult,
                              EvaluationScore)
from mars.data.eval_repo import EvalRepository
# TODO redesign import
from mars.service.service import run_baseline


class Evaluator:
    def __init__(self,
                 repo: EvalRepository,
                 base_url: str,
                 system_message: str,
                 lms: list[str]):
        self.repo = repo
        self.base_url = base_url
        self.system_message = system_message
        self.lms = lms

    @staticmethod
    def read_docx(docx_path: Path):
        doc = Document(docx_path)
        text = ''.join([para.text for para in doc.paragraphs])
        return text

    def run_eval(self):
        run = self.repo.get_latest_run()
        for docx_path in DOCX_DIR.glob('*.docx'):
            text = self.read_docx(docx_path)
            print('evaluating {}'.format(docx_path))
            eval_doc = EvaluationDocument(run=run,
                                          server=self.base_url,
                                          filename=docx_path.name,
                                          system_message=self.system_message)
            eval_results = []
            for lm_name in self.lms:
                print('lm_name: ', lm_name)
                res_chat = run_baseline(base_url=self.base_url,
                                        lm_name=lm_name,
                                        system_message=self.system_message,
                                        query=text)
                result = EvaluationResult(lm_name=lm_name,
                                          output=res_chat)
                eval_results.append(result)
            self.repo.save_eval(eval_doc, eval_results)
