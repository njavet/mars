# project imports
from mars.utils.prompt import get_prompt
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm
        self.rag = None

    def run_query(self, query: str) -> str:
        if self.rag:
            prompt = get_prompt('rag')
            docs = self.rag.retrieve_documents(query)
            full_prompt = prompt.format(doc_text=docs,
                                        query=query)
        else:
            prompt = get_prompt('evaluation')
            full_prompt = prompt.format(doc_text=query)
        return self.lm.generate(full_prompt)

    def set_rag(self, rag: RAG):
        self.rag = rag


def get_agent(lm_name, base_url, enable_rag, session):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    if enable_rag:
        repo = Repository(session=session)
        rag = RAG(repo)
        agent.set_rag(rag)
    return agent
