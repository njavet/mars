from fastapi.logger import logger

# project imports
from mars.core.conf import SCORE_KEYS
from mars.core.deps import fetch_documents
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
        self.agentic = agentic
        self.run = self.repo.get_latest_run()
        self.eval_params = {'temperature': 0.0,
                            'num_ctx': 16384,
                            'top_k': 16,
                            'top_p': 0.5,}

    def run_eval(self):
        logger.info(f'starting eval...{self.run}')
        for filename, content in self.docs.items():
            self.eval_and_save(filename, content)
            logger.info(f'\n--->>> EVAL DONE FOR DOC {filename}...\n')

    def eval_doc_with_llm(self, text: str, llm: OllamaLLM) -> str:
        logger.info(f'running {llm.model_name}...')
        messages = [Message(role='system', content=self.system_message),
                    Message(role='user', content=text)]
        res = llm.chat(messages,
                       options=self.eval_params)
        return res

    def eval_doc_with_agent(self, text: str, llm: OllamaLLM) -> str:
        logger.info(f'running {llm.model_name}...')
        messages = [Message(role='system', content=self.system_message),
                    Message(role='user', content=text)]
        agent = Agent(llm=llm, messages=messages)
        res = agent.generate_res()
        return res

    def eval_and_save(self, filename: str, text: str):
        outputs = {}
        for llm in self.llms:
            if self.agentic:
                res = self.eval_doc_with_agent(text, llm)
            else:
                res = self.eval_doc_with_llm(text, llm)
            outputs[llm.model_name] = res
        result = EvalDoc(run=self.run,
                         server=self.base_url,
                         filename=filename,
                         system_message=self.system_message,
                         models=outputs)
        self.repo.save_eval_doc(result)

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
