from fastapi.logger import logger

# project imports
from mars.utils.prompt import load_system_prompt
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm
        self.rag = None

    def run_query(self,
                  enable_rag: bool,
                  preprompt: str,
                  query: str) -> str:
        logger.debug(f'[Agent] Running query with RAG: {enable_rag}')
        logger.debug(f'[Agent] Query: {query}')

        if enable_rag:
            docs = self.rag.retrieve_documents(query)
            logger.debug(f'[Agent] Retrieved docs...')
            system_prompt = load_system_prompt('rag')['text'].format(docs=docs, query=query)
        else:
            system_prompt = load_system_prompt('standard')['text'].format(query=query)

        full_prompt = '\n'.join([preprompt, system_prompt])

        res = self.lm.generate(full_prompt)
        logger.debug(f'[Agent] LLM response generated...')
        return res

    def set_rag(self, rag: RAG):
        self.rag = rag


def get_agent(base_url, lm_name, session):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    repo = Repository(session=session)
    rag = RAG(repo)
    agent.set_rag(rag)
    return agent
