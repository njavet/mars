from collections import defaultdict
from docx import Document
from fastapi.logger import logger

# project imports
from mars.conf.conf import DOCX_DIR
from mars.schemas import EvalDoc
from mars.data.eval_repo import EvalRepository
from mars.service.lm import LanguageModel, get_lm_names
from mars.service.parsing import clean_medical_body


class Evaluator:
    def __init__(self,
                 base_url: str,
                 system_message: str,
                 chat_api: bool = True,
                 system_message_role: str = 'user'):
        self.repo = EvalRepository()
        self.base_url = base_url
        self.system_message = system_message
        #self.lms = [LanguageModel(name=lm_name, base_url=self.base_url)
        #            for lm_name in get_lm_names(self.base_url)]
        self.lms = [LanguageModel(name=lm_name, base_url=self.base_url)
                    for lm_name in ['openhermes:latest', 'llama3.1:8b']]
        self.chat_api = chat_api
        self.system_message_role = system_message_role

    def run_eval(self):
        run = self.repo.get_latest_run()
        logger.info(f'starting eval...')
        for docx_path in DOCX_DIR.glob('*.docx'):
            doc = Document(docx_path)
            logger.info(f'evaluating doc {docx_path.name}...')
            lms_output = self.eval_doc(doc)
            result = EvalDoc(run=run,
                             server=self.base_url,
                             filename=docx_path.name,
                             system_message=self.system_message,
                             chat_api=self.chat_api,
                             system_message_role=self.system_message_role,
                             lms=lms_output)

            self.repo.save_eval_doc(result)

    def eval_doc(self, doc: Document) -> dict:
        dix = clean_medical_body(doc)
        outputs = defaultdict(list)
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
        lms_output = {lm.name: '\n'.join(outputs[lm.name]) for lm in self.lms}
        return lms_output


class EvalCollector:
    def __init__(self):
        self.repo = EvalRepository()

    def get_runs_list(self) -> list[int]:
        return list(range(self.repo.get_latest_run()))

    def get_eval_docs(self, run: int) -> list[EvalDoc]:
        return self.repo.get_eval_docs(run)
