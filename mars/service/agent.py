# project imports
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm
        self.rag = None

    def run_query(self, query: str, preprompt: str | None = None) -> str:
        if self.rag:
            docs = self.rag.retrieve_documents(query)
            full_prompt = preprompt.format(doc_text=docs,
                                           query=query)
        else:
            full_prompt = preprompt.format(doc_text=query)
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
