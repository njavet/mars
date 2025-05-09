import json
from pathlib import Path
from collections import defaultdict
from docx import Document

# project imports
from mars.conf.conf import DOCX_DIR
from mars.schemas import EvalDoc
from mars.data.eval_repo import EvalRepository
from mars.service.lm import LanguageModel
from mars.service.parsing import clean_medical_body


class Evaluator:
    def __init__(self,
                 repo: EvalRepository,
                 base_url: str,
                 system_message: str,
                 lm_names: list[str]):
        self.repo = repo
        self.base_url = base_url
        self.system_message = system_message
        self.lm_names = lm_names

    def run_eval(self,
                 chat_api: bool = True,
                 system_prompt_injection: str = 'user'):
        run = self.repo.get_latest_run() + 1
        lms = [LanguageModel(name=lm_name, base_url=self.base_url)
               for lm_name in self.lm_names]

        for docx_path in DOCX_DIR.glob('*.docx'):
            doc = Document(docx_path)
            dix = clean_medical_body(doc)
            outputs = defaultdict(list)
            for lm in lms:
                for section, lines in dix.items():
                    if chat_api:
                        res = lm.chat(system_message=self.system_message,
                                      query='\n'.join(lines),
                                      system_prompt_injection=system_prompt_injection)
                    else:
                        # TODO implement generate
                        res = {}
                    outputs[lm.name].append(res['message']['content'])
            lms_output = {lm.name: '\n'.join(outputs[lm.name]) for lm in lms}
            result = EvalDoc(run=run,
                             server=self.base_url,
                             filename=docx_path.name,
                             system_message=self.system_message,
                             chat_api=chat_api,
                             system_prompt_injection=system_prompt_injection,
                             lms=lms_output)
            self.repo.save_eval_doc(result)
