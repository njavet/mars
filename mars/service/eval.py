from sqlalchemy.orm import Session
import json
from pathlib import Path
from collections import defaultdict
from docx import Document

# project imports
from mars.conf.conf import DOCX_DIR
from mars.schemas import EvalDoc
from mars.data.eval_repo import EvalRepository
# TODO redesign import
from mars.service.service import run_baseline
from mars.utils.helpers import clean_medical_body, create_result_dir


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

    @classmethod
    def from_session(cls, session: Session):
        return cls(EvalRepository(session))


    def run_eval(self):
        run = self.repo.get_latest_run() + 1
        for docx_path in DOCX_DIR.glob('*.docx'):
            doc = Document(docx_path)
            dix = clean_medical_body(doc)
            eval_doc = EvalDocTable(run=run,
                                    server=self.base_url,
                                    filename=docx_path.name)
            lms = defaultdict(list)
            for lm_name in self.lms:
                for k, v in dix.items():
                    res_chat = run_baseline(base_url=self.base_url,
                                            lm_name=lm_name,
                                            system_message=self.system_message,
                                            query='\n'.join(v))
                    lms[lm_name].append(res_chat)
                result = EvalDoc(filename=docx_path.name,
                                 system_message=self.system_message,
                                 lms={lm_name: '\n'.join(lms[lm_name])})
            self.repo.save_eval(eval_doc)
            result_dir = create_result_dir(run)
            output_path = Path.joinpath(result_dir, docx_path.stem + '.json')
            # TODO empty result
            with open(output_path, 'w') as f:
                json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
