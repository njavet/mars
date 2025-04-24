# project imports
from mars.utils.prompt import get_prompt
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel, rag: RAG):
        self.lm = lm
        self.rag = rag

    def run_query(self, query: str) -> str:
        prompt = get_prompt()
        docs = self.rag.retrieve_documents(query)
        full_prompt = prompt.format(doc_text=docs,
                                    query=query)
        return self.lm.generate(full_prompt)


def get_agent(lm_name, base_url, session):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    repo = Repository(session=session)
    rag = RAG(repo)
    agent = Agent(lm, rag)
    return agent
