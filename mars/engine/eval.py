import json
from fastapi.logger import logger
import time

from prompt_toolkit import output

# project imports
from mars.core.conf import SCORE_KEYS
from mars.core.ref import ref_complete
from mars.core.deps import fetch_documents, psychopharma
from mars.schema.eval import EvalDoc, ScoreEntry, Message
from mars.db.eval_repo import EvalRepository
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.parsing import parse_text_to_llm_input
from mars.engine.agent import Agent


class Evaluator:
    def __init__(self,
                 repo: EvalRepository,
                 llms: list[OllamaLLM],
                 base_url: str,
                 system_message: str,
                 dtype: str,
                 agentic: bool):
        self.repo = repo
        self.llms = llms
        self.base_url = base_url
        self.system_message = parse_text_to_llm_input(system_message)
        self.docs = fetch_documents(dtype)
        # self.docs = psychopharma()
        self.agentic = agentic
        self.run = self.repo.get_latest_run()

    def run_eval(self):
        logger.info(f'starting eval...{self.run}')
        for file, content in self.docs.items():
            logger.info(f'\n--->>> EVAL START FOR DOC {file}...\n')
            self.eval_and_save(file, content)
            logger.info(f'\n--->>> EVAL DONE FOR DOC {file}...\n')
        self.save_initial_scores()

    def eval_doc_with_llm(self, text: str, llm: OllamaLLM) -> str:
        logger.info(f'running {llm.model_name}...')
        messages = [Message(role='system', content=self.system_message),
                    Message(role='user', content=text)]
        res = llm.chat(messages)
        return res

    def eval_doc_with_agent(self, text: str, llm: OllamaLLM) -> str:
        logger.info(f'running {llm.model_name}...')
        messages = [Message(role='system', content=self.system_message),
                    Message(role='user', content=text)]
        agent = Agent(llm, messages)
        res = agent.generate_res()
        return res

    def eval_and_save(self, filename: str, text: str):
        outputs = {}
        exec_times = {}
        for llm in self.llms:
            s = time.time()
            if self.agentic:
                res = self.eval_doc_with_agent(text, llm)
            else:
                res = self.eval_doc_with_llm(text, llm)
            e = time.time()
            print(f'exec time for {filename} and {llm.model_name}: {e - s}')
            outputs[llm.model_name] = res
            exec_times[llm.model_name] = e - s
        result = EvalDoc(run=self.run,
                         server=self.base_url,
                         filename=filename,
                         system_message=self.system_message,
                         models=outputs,
                         exec_times=exec_times)
        self.repo.save_eval_doc(result)
        self.automatic_eval(result)

    def save_initial_scores(self):
        for file_name in self.docs.keys():
            scores = []
            for llm in self.llms:
                scores.append(self.init_scores(file_name, llm.model_name))
            self.repo.save_scores(scores)

    def init_scores(self, filename: str, model_name: str) -> ScoreEntry:
        scores = {key: 0 for key in SCORE_KEYS}
        return ScoreEntry(run=self.run,
                          filename=filename,
                          model_name=model_name,
                          scores=scores)

    def automatic_eval(self, result):
        match result.filename:
            case 'fehlende_psychopharmakologie':
                self.create_scores(result, 'Ad Psychopharmakologie')
            case 'fehlender_verlauf':
                self.create_scores(result, 'Ad Verlauf')
            case 'fehlende_substanzanamnese':
                self.create_scores(result, 'Drogen und Genussmittel')
            case 'fehlende_vorgeschichte':
                self.create_scores(result, 'Psychiatrische Vorgeschichte')
            case 'unvollstaendige_diagnosen':
                self.create_scores(result, 'Diagnosen')
            case 'vollstaendig_mit_anmerkungen':
                self.create_scores(result)
            case 'vollstaendig_ohne_anmerkungen':
                self.create_scores(result)
            case _:
                print(result.filename)
                raise NotImplementedError

    def create_scores(self, result: EvalDoc, keyword=None):
        scores_lst = []
        for llm_name, res in result.models.items():
            scores = {key: 0 for key in SCORE_KEYS}
            try:
                dix = json.loads(res)
            except json.JSONDecodeError:
                scores['irrelevant'] = 1
            else:
                scores['prompt_alignment'] = 1
                for key in dix.keys():
                    if key not in ref_complete.keys():
                        scores['irrelevant'] = 1
                if keyword is None or keyword not in dix.keys():
                    scores['false_positives'] = sum(dix.values())
                    scores['true_negatives'] = len(dix) - sum(dix.values())
                elif dix[keyword] == 1:
                    scores['true_positives'] = 1
                    scores['false_positives'] = sum(dix.values()) - 1
                else:
                    scores['false_negatives'] = 1
                    scores['false_positives'] = sum(dix.values()) - 1
            se = ScoreEntry(run=result.run,
                            filename=result.filename,
                            model_name=llm_name,
                            scores=scores)
            scores_lst.append(se)
        self.repo.save_scores(scores_lst)
